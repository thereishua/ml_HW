from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = FastAPI(title="招聘数据分析API", version="1.0.0")

# 创建临时目录存储生成的文件
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)


def cleanup_temp_files():
    """清理临时文件"""
    for file in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"清理文件错误: {e}")

@app.post("/analyze/salary_by_district")
async def analyze_salary_by_district(file: UploadFile = File(...)):
    """按地区统计薪资"""

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    salary_stats = df.groupby('district')['salary'].agg([
        ('平均薪资', 'mean'),
        ('最低薪资', 'min'),
        ('最高薪资', 'max'),
        ('职位数量', 'count')
    ]).round(2)

    # 重置索引
    salary_stats = salary_stats.reset_index()

    # 生成Excel文件
    filename = f"salary_stats_analyzed.xlsx"
    filepath = os.path.join(TEMP_DIR, filename)

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        salary_stats.to_excel(writer, sheet_name='薪资统计', index=False)

        # 添加原始数据sheet
        df[['district', 'salary']].to_excel(writer, sheet_name='原始数据', index=False)

    return FileResponse(
        filepath,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=f"各地区薪资统计.xlsx")


@app.post("/analyze/company_count_chart")
async def analyze_company_count_chart(file: UploadFile = File(...)):
    """按地区公司数量生成柱状图"""
    # 读取CSV文件
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    # 按地区统计公司数量
    company_counts = df.groupby('district')['companyId'].nunique().sort_values(ascending=False)

    # 生成柱状图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.figure(figsize=(12, 8))
    company_counts.plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)

    plt.title('各地区公司数量统计', fontsize=16, fontweight='bold')
    plt.xlabel('地区', fontsize=12)
    plt.ylabel('公司数量', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)

    # 在柱子上显示数值
    for i, v in enumerate(company_counts):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

    plt.tight_layout()

    # 保存图片
    filename = f"company_chart.png"
    filepath = os.path.join(TEMP_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    return FileResponse(
        filepath,
        media_type='image/png',
        filename=f"各地区公司数量统计图.png")


@app.get("/")
async def root():
    """返回前端页面"""
    return FileResponse('static/index.html')


# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)