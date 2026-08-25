# 考勤打卡记录爬取工具

自动爬取考勤系统打卡记录，计算加班时长百分比。

## 功能

- 自动登录考勤系统爬取打卡记录
- 支持增量爬取（只爬取缺失日期）
- 自动识别周末调休工作日
- 计算加班时长百分比
- 生成CSV打卡记录文件

## 环境要求

- Python 3.10+
- 系统已安装 Edge 或 Chrome 浏览器
## Clone
```bash
git clone https://github.com/HXBJ1737/attendance.git
```
## 安装

```bash
uv venv
uv pip install -r requirements.txt
```

## 使用

### 运行GUI

```bash
python main.py
```

### 打包为exe

```bash
./build.bat
```

打包后在 `dist/` 目录生成 `AttendanceScraper.exe`。

### 配置说明

| 字段 | 说明 |
|------|------|
| 工号 | 登录账号 |
| 密码 | 登录密码 |
| 起始日期 | 查询开始日期 (YYYY-MM-DD) |
| 终止日期 | 查询结束日期 (YYYY-MM-DD) |
| 加班起算时间 | 正常下班时间 (默认17:20) |
| 未打卡工作日天数 | 居家办公等未打卡天数 |

## 加班计算规则

- **工作日**：加班 = 下班打卡时间 - 17:20
- **周末**：加班 = 下班打卡时间 - 上班打卡时间
- **调休工作日**：按工作日规则计算（自动识别）

## 文件说明

```
├── main.py          # GUI入口
├── scraper.py       # 爬取和计算逻辑
├── calc.py          # 加班百分比计算器
├── build.bat        # 打包脚本
├── run.bat          # 运行已打包程序
├── config.json      # 配置文件
└── requirements.txt # Python依赖
```
