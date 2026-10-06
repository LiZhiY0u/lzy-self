新情境题：一个 C 工程包含以下两个源文件。

`main.c`：
```c
int read_value(void);

int main(void)
{
    return read_value();
}
```

`sensor.c`：
```c
static int read_value(void)
{
    return 7;
}
```

在支持标准 C 的 GCC 环境中，依次执行：
```sh
gcc -c main.c -o main.o
gcc -c sensor.c -o sensor.o
gcc main.o sensor.o -o app
```

这个工程能否生成可执行文件？请独立说明这三条命令各自的结果及原因。
