先在当前目录的 **Windows PowerShell** 中执行第 1 步；我不会代你执行。

```powershell
Get-ChildItem -LiteralPath '.\logs' -Filter '*.log' -File |
    Sort-Object -Property LastWriteTime -Descending |
    Select-Object LastWriteTime, Length, Name
```

这条命令列出 `logs` 目录直接包含的 `.log` 文件，按最后修改时间从新到旧排列，显示修改时间、文件大小（字节）和文件名；不递归搜索子目录。这里把“最新”定义为最后修改时间最晚。

预期会看到一个文件列表，第一行文件是下一步要查看的候选。如果没有匹配文件，可能没有任何输出；如果出现报错，保留报错原文。

请把实际输出回传，我再根据列出的文件指导你读取最新文件最后 20 行。现在还没有输出，不能确认目录中的文件或哪一个最新。
