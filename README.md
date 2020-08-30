# LNTU-API
LNTU-API Online Demo: [https://api.liaoguoyin.com/docs](https://api.liaoguoyin.com/docs)



An elegant backend API of [LNTU Course Management Information System](http://202.199.224.119:8080/eams/loginExt.action) and [LNTU Students Quality Expansion Activity Management System](http://202.199.224.119:8080/eams/loginExt.action).




## How to Deploy

1. Clone the repo to local: `git clone https://github.com/LiaoGuoYin/LNTUME`

2. Change to the root directory of the project, then Install requirements.txt: `pip3 install -r requirements.txt`

3. Copy `config-template.yaml` to `config.yaml`, then fill in your own db configuration and user account.

4. (Optional) Run pytest: `python3 -m pytest`

5. Run Server: `python3 -m uvicorn app.main:app`

6. Then you can go to Brower to inspect the swagger docs of local API: http://localhost:8000/docs

   


## Scheduling
- With Python crawling student's info:
    - [x] login
    - [x] exam scores
    - [x] personal information
    - [ ] teaching plannings
    - [x] class table
    - [ ] class room
    - [ ] exam plannings
    - [ ] school calendar
    - [ ] CET scores
    - [ ] public notification

- Others:
    - [ ] SunnyRunning(AiPao app)
    
    - [ ] Student Quality expansion Spider
    
    - [ ] Water-card Balance
    
      
    
## License

[GPL v3](LICENSE)
