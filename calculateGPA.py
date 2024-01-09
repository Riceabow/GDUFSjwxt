import pandas as pd


def calculate_gpa(grade):
    # grade = int(grade)
    if grade >= 90:
        return 4.0  # A+
    elif grade >= 85:
        return 3.7  # A
    elif grade >= 82:
        return 3.3  # A-
    elif grade >= 78:
        return 3.0  # B+
    elif grade >= 75:
        return 2.7  # B
    elif grade >= 72:
        return 2.3  # B-
    elif grade >= 68:
        return 2.0  # C+
    elif grade >= 65:
        return 1.7  # C
    elif grade >= 62:
        return 1.3  # C-
    elif grade >= 58:
        return 1.0  # D+
    else:
        return 0.0  # F


class CalGPA:
    total_credits = 0
    total_GPA = 0.0
    semester_credits = pd.DataFrame([])
    semester_GPA = pd.DataFrame([])
    meanGPA = 0.0
    meanGPA_eachSemester = pd.DataFrame([])
    df = pd.DataFrame([])
    total_situation = {
        "已修读学分": total_credits,
        "总平均绩点": meanGPA
    }
    detailed_situation = [semester_credits, semester_GPA]

    resultList = {"total": total_situation,
                  "detailed": total_situation}

    def __init__(self, df):
        self.df = df
        df['成绩'] = df['成绩'].astype(float)
        df['学分'] = df['学分'].astype(int)

    def calEachGPA(self):
        self.df['绩点'] = self.df['成绩'].apply(calculate_gpa)
        return self.df

    def calMeanGPA(self):
        # 按'开课学期'分组，计算每个学期的平均绩点
        # 平均学分绩点（GAP）=∑（课程绩点*课程学分）/∑课程学分
        self.total_credits = self.df['学分'].sum()  # 学分求和
        self.df['加权绩点'] = self.df['绩点'] * self.df['学分']  # 计算加权绩点
        self.total_GPA = self.df['加权绩点'].sum()  # 计算加权绩点总和
        self.meanGPA = self.total_GPA / self.total_credits  # 计算平均绩点（所有课程的平均绩点）

        self.semester_credits = self.df.groupby('开课学期')['学分'].sum()  # 对学期内的学分求和
        self.semester_GPA = self.df.groupby('开课学期')['加权绩点'].sum()  # 计算学期内加权绩点总和
        self.meanGPA_eachSemester = self.semester_GPA / self.semester_credits # 计算平均绩点（每学期的平均绩点）
        self.meanGPA_eachSemester.name = "学期内平均绩点"
        self.total_situation = {
            "已修读学分": self.total_credits,
            "总平均绩点": self.meanGPA
        }
        self.detailed_situation = [self.semester_credits, self.meanGPA_eachSemester]

        self.resultList = {"total": self.total_situation,
                           "detailed": self.detailed_situation}
        return self.resultList
