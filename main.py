import streamlit
from GDUFSjwxt import jwxt
import streamlit.web.bootstrap as bootstrap
if __name__ == '__main__':
    jwxt = jwxt(id="", psw="")  # 连接教务系统，参数id 是学号，psw是密码，均为字符串
    jwxt.login()  # 登录教务系统，手动填写获取到的验证码verifycode.jpg;想实现自动化可自行添加字符识别模型
    jwxt.QScoreList()  # 获取课程成绩页面
    jwxt.save_scores()  # 保存成绩信息，保存在项目路径下data文件夹下，all_scores.csv

    streamlit._is_running_with_streamlit = True
    bootstrap.run('app.py', 'streamlit run', [], {})
