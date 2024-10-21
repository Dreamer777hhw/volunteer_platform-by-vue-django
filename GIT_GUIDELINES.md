# Git 规范

## 分支命名

- **主分支**：`main`  
  用于发布的稳定版本。

- **开发分支**：`develop`  
  用于开发的主要分支，所有的功能分支合并到此分支。

- **功能分支**：`feature/<issue-id>-<description>`  
  例如：`feature/123-add-login-form`  
  用于开发新功能。每个功能分支应基于 `develop` 分支创建。

- **修复分支**：`fix/<issue-id>-<description>`  
  例如：`fix/123-fix-login-bug`  
  用于修复 bug。每个修复分支应基于 `develop` 分支创建。

## 提交信息

提交信息应简洁明了，请遵循以下格式：

<类型>(<范围>): <内容>

### 类型

 - feat： 新功能
 - fix： 修复问题
 - docs： 文档变更
 - style： 改变样式
 - test： 添加测试
 - refactor： 重构

### 示例
```git
feat(auth): add Login.vue
feat(auth): add login form in Login.vue
docs(git): add GIT_GUIDELINES.md
```

## 开发要求

如果您希望开发一个功能，请遵循以下方式：

```git
git checkout develop
git pull origin develop
git checkout -b feature/A-add-something
...
git add path/to/your/files
git commit -m "feat(A): add something"
git push origin feature/A-add-something
# 提交功能A的合并请求
```

