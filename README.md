# LNTU-API
Online Demo: [https://lntu.me](https://lntu.me)

An elegant backend API of [LNTU Course Management Information System](http://202.199.224.119:8080/eams/loginExt.action) and [LNTU Students Quality Expansion Activity Management System.](http://202.199.224.19:8080/)


## How to Deploy

1. Clone the repo to local: `git clone https://github.com/LiaoGuoYin/LNTUME`

2. Change to the root directory of the project, then installing requirements: `pip3 install -r requirements.txt`

3. Copy `config-template.yaml` to `config.yaml`, then filling your own db and account config in.

4. (Optional) Run pytest: `python3 -m pytest`

5. Run Server: `python3 -m uvicorn app.main:app`

6. Then you can inspect the swagger docs of local API in your browser: http://localhost:8000/docs

   


## Scheduling
- With Python crawling student's info:
    - [x] login
    - [x] exam score
    - [x] personal information
    - [ ] teaching plannings
    - [x] course table
    - [x] class room
    - [ ] exam plannings
    - [ ] school calendar
    - [ ] CET scores
    - [x] public notice

- Others:
    - [x] SunnyRunning(AiPao app)
    - [x] Student Quality expansion Spider
    - [ ] Water-card Balance
    
      
  
## Requirements
  
1. MySQL or Mariadb(10.3+)
2. Python(3.7.2+)


## License
[GPL v3](LICENSE)

注意：对于基于本项目 **衍生、再发行的所有项目、所有子节点项目和使用了 LNTU-API 提供的部分开源组件**  的项目，其需公开注明 LNTU-API 标识。