---
title: V8 是如何进行正则表达式匹配的(施工中)
date: 2025-08-26 00:20
excerpt: TODO
category: 前端
mermaid: true
---
# 背景
最近在写油猴脚本，遇到需要大量进行正则表达式匹配的场景，因为油猴脚本在用户端运行，所以希望能扣一点性能出来，哪怕能节约 1 ms 也是好的

这里就有一个优化场景：`new RegExp(/a/).test('abc')` 和 `new RegExp(/abc/).test('abc')` 都会返回 `true`，那么是否需要用开发者的先验，尽量在正则表达式中提供更多的信息，节约匹配时的计算量？

然后就想到 [leetcode 中做过正则表达式匹配的题](https://leetcode.cn/problems/regular-expression-matching/)，但只是 `.` 和 `*` 的简单场景，正好研究一下生产环境中实际的正则表达式匹配是怎么做的


# 原理
从编译原理视角，正则表达式（Regular Expression, RE）描述的是"正则语言"，对应可被有限自动机识别：

- 正则 → ε-NFA（Thompson 构造法：递归地为每个正则子表达式构造 NFA 片段，用 ε-转换连接）
- ε-NFA → DFA（子集构造，可选最小化）
- 用自动机在输入上“运行”即可完成匹配（锚定匹配与搜索仅是起始位置选择与边界条件不同）

教科书上的“RE→NFA→DFA→匹配”给了一个线性时间、确定执行的理想范式，但在工程实践中很少直接构造整张 DFA，原因是：
- 状态爆炸：某些模式的 DFA 状态数指数级，内存不可控
- 特性缺失：DFA 框架天然不支持“回溯语义”“反向引用”等非正规特性

因此主流引擎会在三条路线中权衡：
- 回溯 VM：沿语法树深度优先搜索，功能强（支持环视、反向引用），但最坏情形指数时间（灾难性回溯）
- NFA 仿真（非回溯）：像 RE2 一样用工作队列同时推进多个 NFA 状态，时间线性但不支持反向引用等
- DFA/字面量特化：对纯字面量或可归约成固定字符串集的情形走字符串搜索（如 Boyer–Moore/IndexOf）

结合 V8 的实现，可以更精确地理解“V8 干了什么”：

- V8 的主力引擎叫 Irregexp。它将正则表达式解析成 AST，然后编译为字节码（解释执行）或机器码（JIT 编译）。执行时采用回溯算法，但通过大量优化减少回溯开销：包括快速失败检查、前缀优化、字符类预检查等
- 对于完全"无元字符"的纯字面量，V8 在编译期将类型标记为 ATOM，直接退化成字符串搜索（内部走 `StringIndexOf` 的快路径）。这就是为什么"/a/"与"/abc/"看起来都很快——它们都可能走同一条"字面量搜索"通道。
- 为避免灾难性回溯，V8 实现了一个实验性的线性时间引擎。当正则表达式不包含反向引用、环视断言等复杂特性时，会尝试使用该引擎进行匹配。该引擎基于 NFA 仿真，能保证线性时间复杂度。如果实验引擎无法处理，会回退到传统的 Irregexp 引擎。
- 实际执行前，V8 会对待匹配的字符串做"扁平化/直达化"（把 `ConsString/SlicedString` 变成连续内存），并选择与之匹配的代码版本（Latin1/UC16）。匹配产生的每个捕获组用一对"寄存器（起始/结束偏移）"记录，最终填充到 `last_match_info`。


V8 这里的代码看起来很难受，是因为并非直接写“匹配循环”，而是在操作编译器：
- 解析与分析正则
- 为不同输入与标志位生成不同形态的字节码/机器码
- 在运行时按类型（IRREGEXP/ATOM/EXPERIMENTAL）调度到最合适的执行引擎


# 实现细节
## 执行流程概览
这边理应是一个 mermaid 图，但是因为图太大了，直接在这里预览会看不清，所以去[这里](https://github.com/chesha1/blog/blob/main/mermaid/regex-1.md)看吧


## 详细调用链

### 1. 入口点：RegExpPrototypeTest

**文件位置**: `src/builtins/regexp-test.tq:11-27`

```cpp
transitioning javascript builtin RegExpPrototypeTest(
    js-implicit context: NativeContext, receiver: JSAny)(
    string: JSAny): JSAny {
  const methodName: constexpr string = 'RegExp.prototype.test';
  const receiver = Cast<JSReceiver>(receiver)
      otherwise ThrowTypeError(
      MessageTemplate::kIncompatibleMethodReceiver, methodName, receiver);
  const str: String = ToString_Inline(string);
  if (IsFastRegExpPermissive(receiver)) {
    RegExpPrototypeExecBodyWithoutResultFast(
        UnsafeCast<JSRegExp>(receiver), str)
        otherwise return False;
    return True;
  }
  const matchIndices = RegExpExec(receiver, str);
  return SelectBooleanConstant(matchIndices != Null);
}
```

**执行步骤**:
1. 类型检查：确保 `receiver` 是 `JSReceiver`
2. 字符串转换：将输入参数转换为字符串
3. 快速路径检查：调用 `IsFastRegExpPermissive()` 
4. 根据检查结果选择执行路径

### 2. 快速路径检查：IsFastRegExpPermissive

**文件位置**: `src/builtins/regexp.tq`（宏声明），具体快速检查逻辑在 `src/builtins/builtins-regexp-gen.cc`

在 Torque 中导出 `IsFastRegExpPermissive/IsFastRegExpForMatch/IsFastRegExpForSearch/IsFastRegExpStrict` 这些宏，它们内部通过 CSA 的 `BranchIfFastRegExp_*` 实现在 C++ 中完成实际检查。

**核心实现**: `src/builtins/builtins-regexp-gen.cc` 中的 `RegExpBuiltinsAssembler::BranchIfFastRegExp` 及其包装 `BranchIfFastRegExp_Permissive/Strict/ForMatch/ForSearch`

#### 什么是"优化的执行路径"？

快速路径检查确定是否可以跳过昂贵的动态查找，直接使用内置的优化实现。具体检查以下条件：

实际检查步骤：
- 强制慢速路径开关：`GotoIfForceSlowPath(if_ismodified);`
- Species protector：`GotoIf(IsRegExpSpeciesProtectorCellInvalid(), if_ismodified);`
- 初始 map 相等：从 `NativeContext::REGEXP_FUNCTION_INDEX` 取初始 map，`TaggedEqual(map, initial_map)`；不相等则慢速。
- lastIndex 为正 Smi：`FastLoadLastIndexBeforeSmiCheck` 读取对象内字段，要求 `TaggedIsPositiveSmi`，否则慢速。
- 原型检查：使用 `PrototypeCheckAssembler` 根据不同 flags 检查 `RegExp.prototype` 上关键属性（如 exec/search/match）是否保持 const 或恒等。

#### 两种检查模式

两种模式及差异：
- Strict（严格）：`kCheckPrototypePropertyConstness`，只检查描述符“常量性”（不做值等同性检查）。
- Permissive（宽松）：`kCheckFull = Constness | Identity`，在常量性失败时，允许继续做“值恒等”检查，若值仍与初始内建函数相同，则仍可走快路径。
另外，`ForMatch/ForSearch` 还会附加检查相应的 `@@match/@@search` 描述符索引与初始值匹配。

#### 为什么需要这些检查？

**性能优化的前提**：
- 避免属性查找：直接调用内置函数，无需在原型链上查找
- 跳过类型转换：已知数据类型，避免动态转换
- 内联优化：编译器可以内联调用，减少函数调用开销
- 避免用户代码执行：防止 getter/setter 被调用

**如果检查失败会怎样**：
- 回退到慢速路径（`RegExpExec`）
- 进行完整的属性查找
- 调用可能被重写的方法
- 执行完整的类型检查和转换

### 3A. 快速路径：RegExpPrototypeExecBodyWithoutResultFast

**文件位置**: `src/builtins/regexp.tq:123-129`

```cpp
transitioning macro RegExpPrototypeExecBodyWithoutResultFast(
    implicit context: Context)(regexp: JSRegExp,
    string: String): RegExpMatchInfo labels IfDidNotMatch {
  const lastIndex = LoadLastIndexAsLength(regexp, true);
  return RegExpPrototypeExecBodyWithoutResult(regexp, string, lastIndex, true)
      otherwise IfDidNotMatch;
}
```

**核心函数**: `RegExpPrototypeExecBodyWithoutResult`

**文件位置**: `src/builtins/regexp.tq:86-120`

主要逻辑：
1. 检查 global 或 sticky 标志
2. 如果是 global/sticky，更新 lastIndex
3. 调用 `RegExpExecInternal_Single` 执行匹配

### 3B. 慢速路径：RegExpExec

**文件位置**: `src/builtins/regexp.tq:42-67`

```cpp
transitioning macro RegExpExec(
    implicit context: Context)(receiver: JSReceiver, string: String): JSAny {
  const exec = GetProperty(receiver, 'exec');
  
  typeswitch (exec) {
    case (execCallable: Callable): {
      const result = Call(context, execCallable, receiver, string);
      if (result != Null) {
        ThrowIfNotJSReceiver(
            result, MessageTemplate::kInvalidRegExpExecResult, '');
      }
      return result;
    }
    case (Object): {
      const regexp = Cast<JSRegExp>(receiver) otherwise ThrowTypeError(
          MessageTemplate::kIncompatibleMethodReceiver, 'RegExp.prototype.exec',
          receiver);
      return RegExpPrototypeExecSlow(regexp, string);
    }
  }
}
```

执行步骤：
1. 获取 `exec` 属性
2. 如果 `exec` 是可调用的，直接调用
3. 否则回退到内置的慢速实现

### 4. 核心执行：RegExpExecInternal_Single

**文件位置**: `src/builtins/builtins-regexp-gen.cc`（见 RegExpBuiltinsAssembler::RegExpExecInternal_Single）

关键步骤：
- 读取 `RegExpData`，计算每次匹配所需寄存器数量：`RegistersForCaptureCount(LoadCaptureCount(data))`，并据此分配或借用 `result_offsets_vector`（可能复用静态缓冲或动态分配）。
- 用异常保护块包裹对 `RegExpExecInternal` 的调用；若抛异常，先释放向量再 `Runtime::kReThrow`。
- 若返回 0 次匹配：释放向量，跳转 `if_not_matched`；否则仅允许返回 1（single 模式），并用 `InitializeMatchInfoFromRegisters` 将 offset 写入 `last_match_info`，然后释放向量并返回。
注意：无论成功、失败或异常，`result_offsets_vector` 都会被释放或归还（DEBUG 下还会清零隐式参数）。

### 5. 底层执行引擎：RegExpExecInternal

**文件位置**: `src/builtins/builtins-regexp-gen.cc:625-904`

`RegExpExecInternal` 是正则表达式执行的核心调度器，负责：
1. 字符串预处理
2. 执行引擎选择和分发  
3. 结果处理和错误恢复

## `RegExpExecInternal` 底层执行细节

### 输入验证和字符串预处理

在正则表达式执行之前，V8 需要对输入进行严格的验证和预处理：

**参数验证阶段**
```cpp
// 验证 lastIndex 的有效性和边界检查
CSA_DCHECK(this, IsNumberNormalized(last_index));
CSA_DCHECK(this, IsNumberPositive(last_index));
GotoIf(TaggedIsNotSmi(last_index), &out, GotoHint::kFallthrough);

// 边界检查：lastIndex > string.length 时直接失败
TNode<IntPtrT> int_string_length = LoadStringLengthAsWord(string);
TNode<IntPtrT> int_last_index = PositiveSmiUntag(CAST(last_index));
GotoIf(UintPtrGreaterThan(int_last_index, int_string_length), &out);
```

**字符串扁平化处理**
```cpp
// 字符串扁平化：展开 SlicedString 等复合字符串
ToDirectStringAssembler to_direct(state(), string);
to_direct.ToDirect();
```

这一步骤将复合字符串（如 `SlicedString`、`ConsString`）转换为连续的内存表示，确保后续的模式匹配能够高效访问字符数据。

### 执行引擎分发机制

V8 根据正则表达式的数据类型选择执行引擎，并在需要时回退到运行时：

**引擎类型判断**
```cpp
TNode<Int32T> tag =
  SmiToInt32(LoadObjectField<Smi>(data, RegExpData::kTypeTagOffset));

int32_t values[] = {
  static_cast<uint8_t>(RegExpData::Type::IRREGEXP),
  static_cast<uint8_t>(RegExpData::Type::ATOM),
  static_cast<uint8_t>(RegExpData::Type::EXPERIMENTAL),
};
Label* labels[] = {&next, &atom, &next};
Switch(tag, &unreachable, values, labels, arraysize(values));
```
说明：当类型为 IRREGEXP 或 EXPERIMENTAL 时，都会先走 `&next` 分支，后续由 IR 路径中的返回码决定是否回退到实验引擎（`retry_experimental`）

### 机器码执行路径（IRREGEXP）

对于复杂的正则表达式，V8 会将其编译为优化的机器码：

**IRREGEXP：代码加载和验证**
```cpp
// 1) 根据字符串编码加载对应的编译代码与字节码
if (to_direct.IsOneByte()) {
  var_code = LoadObjectField<CodeT>(data, IrRegExpData::kLatin1CodeOffset);
  var_bytecode = LoadObjectField(data, IrRegExpData::kLatin1BytecodeOffset);
} else {
  var_code = LoadObjectField<CodeT>(data, IrRegExpData::kUc16CodeOffset);
  var_bytecode = LoadObjectField(data, IrRegExpData::kUc16BytecodeOffset);
}

// 2) 检查编译代码是否可用（SANDBOX 与非 SANDBOX 略有不同）
#ifdef V8_ENABLE_SANDBOX
GotoIf(Word32Equal(var_code.value(), Int32Constant(kNullIndirectPointerHandle)),
       &runtime);
#else
GotoIf(TaggedIsSmi(var_code.value()), &runtime);
#endif
```

**本地代码调用与结果处理**
```cpp
// 3) 调用编译后的机器码（或解释器 trampoline），并根据返回码分支
TNode<Int32T> result = CallCFunctionWithoutFunctionDescriptor(...);
TNode<IntPtrT> int_result = ChangeInt32ToIntPtr(result);
var_result = Unsigned(int_result);
static_assert(RegExp::kInternalRegExpSuccess == 1);
static_assert(RegExp::kInternalRegExpFailure == 0);
GotoIf(IntPtrGreaterThanOrEqual(
      int_result, IntPtrConstant(RegExp::kInternalRegExpFailure)),
  &out);
GotoIf(IntPtrEqual(int_result,
         IntPtrConstant(RegExp::kInternalRegExpRetry)),
  &runtime);
GotoIf(IntPtrEqual(int_result,
         IntPtrConstant(RegExp::kInternalRegExpException)),
  &if_exception);
CSA_CHECK(this, IntPtrEqual(int_result, IntPtrConstant(
             RegExp::kInternalRegExpFallbackToExperimental)));
Goto(&retry_experimental);
```

### 字符串搜索优化（ATOM）

对于简单的字符串匹配（ATOM），V8 使用内建的 `StringIndexOf` 进行搜索：

```cpp
// 简单字符串匹配，调用内建 StringIndexOf
BIND(&atom_path);
{
    var_result = RegExpExecAtom(context, CAST(data), string, CAST(last_index),
                               result_offsets_vector, result_offsets_vector_length);
    Goto(&out);
}
```

### 运行时回退机制

当机器码执行失败或不可用时，V8 回退到 C++ 运行时：

**运行时调用设置**
```cpp
BIND(&runtime);
{
    // 设置隐式参数：结果向量
    auto vector_arg = ExternalConstant(
        ExternalReference::Create(IsolateFieldId::kRegexpExecVectorArgument));
    StoreNoWriteBarrier(MachineType::PointerRepresentation(), 
                       vector_arg, result_offsets_vector);
    
    // 调用运行时函数
    TNode<Smi> result_as_smi = CAST(
        CallRuntime(Runtime::kRegExpExec, context, regexp, string, last_index,
                   SmiFromInt32(result_offsets_vector_length)));
    
    var_result = UncheckedCast<UintPtrT>(SmiUntag(result_as_smi));
    Goto(&out);
}
```

### 实验引擎执行路径

V8 支持实验性（包括 linear 标志）正则引擎。该路径可能由两种情况触发：
- IR 引擎返回 `kInternalRegExpFallbackToExperimental`，跳到 `retry_experimental`。
- 正则数据类型为 EXPERIMENTAL（在分发处走 `&next`，后续由 trampoline 或 runtime 执行）。

```cpp
BIND(&retry_experimental);
{
    // 设置隐式参数
    auto vector_arg = ExternalConstant(
        ExternalReference::Create(IsolateFieldId::kRegexpExecVectorArgument));
    StoreNoWriteBarrier(MachineType::PointerRepresentation(),
                       vector_arg, result_offsets_vector);
    
  // 调用实验性正则引擎（一次性执行）
    TNode<Smi> result_as_smi = CAST(CallRuntime(
        Runtime::kRegExpExperimentalOneshotExec, context, regexp, string,
        last_index, SmiFromInt32(result_offsets_vector_length)));
    
    var_result = UncheckedCast<UintPtrT>(SmiUntag(result_as_smi));
    Goto(&out);
}
```

### C++ 运行时深层调用

当需要回退到运行时时，调用链继续深入到 C++ 层：

**Runtime::kRegExpExec** → **RegExp::Exec** → **具体引擎实现**

```cpp
// src/regexp/regexp.cc:RegExp::Exec
std::optional<int> RegExp::Exec(Isolate* isolate, DirectHandle<JSRegExp> regexp,
                                DirectHandle<String> subject, int index,
                                int32_t* result_offsets_vector,
                                uint32_t result_offsets_vector_length) {
  DirectHandle<RegExpData> data(regexp->data(isolate), isolate);
  switch (data->type_tag()) {
    case RegExpData::Type::ATOM:
      return RegExpImpl::AtomExec(isolate, TrustedCast<AtomRegExpData>(data),
                                  subject, index, result_offsets_vector,
                                  result_offsets_vector_length);
    case RegExpData::Type::IRREGEXP:
      return RegExpImpl::IrregexpExec(isolate, TrustedCast<IrRegExpData>(data),
                                      subject, index, result_offsets_vector,
                                      result_offsets_vector_length);
    case RegExpData::Type::EXPERIMENTAL:
      return ExperimentalRegExp::Exec(isolate, TrustedCast<IrRegExpData>(data),
                                      subject, index, result_offsets_vector,
                                      result_offsets_vector_length);
  }
}
```

## 正则表达式执行中的宏系统分析

在V8的正则表达式实现中，大量使用了各种宏来简化代码开发、增强调试能力和提供类型安全。这些宏可以分为几个主要类别：

### 代码生成和控制流宏

#### 1. BIND 宏
**定义位置**: `src/codegen/define-code-stub-assembler-macros.inc`（Debug 与 Release 下宏展开不同）

```cpp
// Debug模式
#define BIND(label) Bind(label, CSA_DEBUG_INFO(label))
// Release模式  
#define BIND(label) Bind(label)
```

**功能**: 将标签绑定到当前代码位置，用于实现跳转目标
**使用示例**: 
- `BIND(&atom_path)` - 绑定原子路径标签
- `BIND(&runtime)` - 绑定运行时回退标签
- `BIND(&retry_experimental)` - 绑定实验引擎重试标签

#### 2. 控制流宏系列
这些宏由CodeStubAssembler基类提供，用于实现条件跳转和分支：

```cpp
// 无条件跳转
Goto(Label* label);

// 条件跳转
GotoIf(TNode<IntegralT> condition, Label* true_label);
GotoIfNot(TNode<IntegralT> condition, Label* false_label);

// 双向分支
Branch(TNode<IntegralT> condition, Label* true_label, Label* false_label);

// 多路分支
Switch(value, &default_label, cases, labels, count);
```

### 断言和调试宏系统

#### 1. CSA_DCHECK 宏
**定义位置**: `src/codegen/define-code-stub-assembler-macros.inc`

```cpp
// Debug模式：完整检查
#define CSA_DCHECK(csa, condition_node, ...) \
  (csa)->Dcheck(condition_node, #condition_node, CSA_DCHECK_ARGS(__VA_ARGS__))

// Release模式：完全移除
#define CSA_DCHECK(csa, ...) ((void)0)
```

**特点**：
- **条件编译**: 仅在DEBUG构建中生效
- **运行时标志控制**: 通过 `v8_flags.debug_code` 开启/关闭
- **源码信息**: 自动包含文件名、行号和条件文本
- **支持额外参数**: 断言失败时可打印相关变量值

**使用示例**：
```cpp
CSA_DCHECK(this, IsNumberNormalized(last_index));
CSA_DCHECK(this, TaggedIsSmi(index), index, length);  // 带调试信息
```

#### 2. CSA_CHECK 宏
**定义位置**: `src/codegen/define-code-stub-assembler-macros.inc`

```cpp
// Debug模式：详细检查
#define CSA_CHECK(csa, x) (csa)->Check([&]() -> TNode<BoolT> { return x; }, #x)

// Release模式：快速检查
#define CSA_CHECK(csa, x) (csa)->FastCheck(x)
```

**特点**：
- **总是执行**: 在所有构建模式下都进行检查
- **安全关键**: 用于不能被优化掉的重要验证
- **性能权衡**: Release模式使用更快的检查方式

#### 3. CSA_SLOW_DCHECK 宏
**定义位置**: `src/codegen/define-code-stub-assembler-macros.inc:83-88`

```cpp
#ifdef ENABLE_SLOW_DCHECKS
#define CSA_SLOW_DCHECK(csa, ...)     \
  if (v8_flags.enable_slow_asserts) { \
    CSA_DCHECK(csa, __VA_ARGS__);     \
  }
#else
#define CSA_SLOW_DCHECK(csa, ...) ((void)0)
#endif
```

**特点**：
- **昂贵检查**: 用于计算成本高的断言
- **双重条件**: 需要编译时和运行时标志都开启
- **精确控制**: 避免在性能测试中影响结果

#### 4. SBXCHECK 宏系列
**定义位置**: `src/sandbox/check.h`

```cpp
// 沙箱模式：使用沙箱专用检查
#ifdef V8_ENABLE_SANDBOX
#define SBXCHECK(condition) SandboxCheck(condition)
#define SBXCHECK_EQ(lhs, rhs) SandboxCheckEq(lhs, rhs)

// 非沙箱模式：降级为普通CHECK
#else
#define SBXCHECK(condition) CHECK(condition)
#define SBXCHECK_EQ(lhs, rhs) CHECK_EQ(lhs, rhs)
#endif
```

**功能**: 沙箱安全检查，确保指针和内存访问的安全性；在 CSA 端有对应的 `CSA_SBXCHECK`，当启用沙箱时等同于 `CSA_CHECK`，否则退化为 `CSA_DCHECK`。

### 函数调用宏

#### 1. CallRuntime 系列
用于从代码生成器调用V8运行时函数：

```cpp
// 调用运行时函数
CallRuntime(Runtime::kRegExpExec, context, regexp, string, last_index);

// 调用实验引擎
CallRuntime(Runtime::kRegExpExperimentalOneshotExec, context, ...);
```

#### 2. CallCFunction 系列
用于调用编译后的机器码或C++函数：

```cpp
// 无描述符调用（用于正则机器码）
CallCFunctionWithoutFunctionDescriptor(code_entry, return_type, args...);

// 有描述符调用
CallCFunction(function_reference, return_type, args...);
```

### Torque 语言特定宏

#### 1. transitioning 关键字
```torque
transitioning javascript builtin RegExpPrototypeTest(
    js-implicit context: NativeContext, receiver: JSAny)(
    string: JSAny): JSAny
```

**功能**: 标记函数可能改变堆状态，需要特殊的垃圾回收处理

#### 2. otherwise 错误处理
```torque
RegExpPrototypeExecBodyWithoutResultFast(
    UnsafeCast<JSRegExp>(receiver), str)
    otherwise return False;
```

**功能**: Torque的异常处理机制，类似于C++的异常或Go的错误返回

#### 3. typeswitch 模式匹配
```torque
typeswitch (exec) {
  case (execCallable: Callable): {
    // 处理可调用对象
  }
  case (Object): {
    // 处理普通对象
  }
}
```

**功能**: 基于类型的模式匹配，编译时类型安全

### 实用工具宏

#### 1. arraysize 宏
**定义位置**: `src/base/macros.h:67`

```cpp
#define arraysize(array) (sizeof(ArraySizeHelper(array)))
```

**功能**: 编译时计算数组大小，类型安全
**使用示例**: `Switch(tag, &unreachable, values, labels, arraysize(values));`

#### 2. IRREGEXP 常量
**使用场景**: 标识使用编译后机器码执行的正则表达式类型
```cpp
case RegExpData::Type::IRREGEXP:
  // 使用编译后的机器码执行
```

### Runtime函数生成宏系统

#### 1. Runtime函数声明宏
**定义位置**: `src/runtime/runtime.h:460-472`

```cpp
#define FOR_EACH_INTRINSIC_REGEXP(F, I)             \
  F(RegExpBuildIndices, 3, 1)                       \
  F(RegExpGrowRegExpMatchInfo, 2, 1)                \
  F(RegExpExecMultiple, 3, 1)                       \
  F(RegExpInitializeAndCompile, 3, 1)               \
  F(RegExpMatchGlobalAtom, 3, 1)                    \
  F(RegExpReplaceRT, 3, 1)                          \
  F(RegExpSplit, 3, 1)                              \
  F(RegExpStringFromFlags, 1, 1)                    \
  F(StringReplaceNonGlobalRegExpWithFunction, 3, 1) \
  F(StringSplit, 3, 1)                              \
  F(RegExpExec, 4, 1)                               \
  F(RegExpExperimentalOneshotExec, 4, 1)
```

**宏参数说明**:
- `F(name, nargs, ressize)`: 函数名、参数数量、返回值大小
- `RegExpExec, 4, 1`: RegExpExec函数，4个参数，返回1个值

#### 2. Runtime枚举生成机制
**定义位置**: `src/runtime/runtime.h:920-927`

```cpp
class Runtime : public AllStatic {
 public:
  enum FunctionId : int32_t {
#define F(name, nargs, ressize, ...) k##name,           // 生成 kRegExpExec = N
#define I(name, nargs, ressize, ...) kInline##name,
    FOR_EACH_INTRINSIC(F) FOR_EACH_INLINE_INTRINSIC(I)  // 展开所有宏
#undef I
#undef F
        kNumFunctions,
  };
```

**生成结果**: 
- `kRegExpExec` - 正则表达式执行函数ID
- `kRegExpExperimentalOneshotExec` - 实验引擎执行函数ID
- 每个函数自动分配唯一的数字ID

#### 3. RUNTIME_FUNCTION宏
**定义位置**: `src/execution/arguments.h:191-193`

```cpp
#define RUNTIME_FUNCTION(Name)                           \
  RUNTIME_FUNCTION_RETURNS_TYPE(Address, Tagged<Object>, \
                                BUILTIN_CONVERT_RESULT, Name)
```

**展开机制**: `src/execution/arguments.h:162-181`
```cpp
#define RUNTIME_FUNCTION_RETURNS_TYPE(Type, InternalType, Convert, Name)   \
  static V8_INLINE InternalType __RT_impl_##Name(RuntimeArguments args,    \
                                                 Isolate* isolate);        \
  Type Name(int args_length, Address* args_object, Isolate* isolate) {     \
    RuntimeArguments args(args_length, args_object);                       \
    return Convert(__RT_impl_##Name(args, isolate));                       \
  }                                                                        \
  static InternalType __RT_impl_##Name(RuntimeArguments args, Isolate* isolate)
```

**使用示例**:
```cpp
// 声明 (在 runtime-regexp.cc:956)
RUNTIME_FUNCTION(Runtime_RegExpExec) {
  // 函数实现
  DirectHandle<JSRegExp> regexp = Cast<JSRegExp>(args.at<Object>(0));
  // ...
}
```

**自动生成的代码**:
```cpp
// 生成的包装函数
Address Runtime_RegExpExec(int args_length, Address* args_object, Isolate* isolate) {
  RuntimeArguments args(args_length, args_object);
  return BUILTIN_CONVERT_RESULT(__RT_impl_Runtime_RegExpExec(args, isolate));
}

// 实际实现函数
static Tagged<Object> __RT_impl_Runtime_RegExpExec(RuntimeArguments args, Isolate* isolate) {
  // 用户编写的实现代码
}
```

#### 4. 外部引用生成机制
Runtime函数通过ExternalReference系统暴露给CodeStubAssembler：

```cpp
// CallRuntime宏会自动解析Runtime::kRegExpExec为对应的C++函数地址
CallRuntime(Runtime::kRegExpExec, context, regexp, string, last_index);

// 等价于直接调用
ExternalReference(Runtime::FunctionForId(Runtime::kRegExpExec), isolate)
```

### 宏代码生成的完整流程

1. **宏声明阶段**: `FOR_EACH_INTRINSIC_REGEXP`定义所有正则相关函数
2. **枚举生成**: 通过宏展开生成`Runtime::kRegExpExec`等枚举值  
3. **函数签名生成**: 自动生成C++函数签名和包装代码
4. **地址查找**: Runtime::FunctionForId将枚举值映射为函数指针
5. **CSA调用**: CodeStubAssembler通过ExternalReference调用C++函数

# 参考文献
https://v8.dev/blog/non-backtracking-regexp

https://v8.dev/blog/speeding-up-regular-expressions

https://regex101.com/

以及再搜索一下 v8 blog 和互联网资源