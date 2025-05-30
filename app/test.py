import pandas as pd

# Загрузка данных
df = pd.read_csv("./data/freelancer_earnings_bd.csv")

# Фильтрация фрилансеров с рейтингом >= 4.5
high_rated = df[df["Client_Rating"] >= 4.5]

# Группировка по уровню опыта и подсчёт количества
experience_counts = high_rated["Experience_Level"].value_counts()

# Нахождение уровня с наибольшим количеством
most_common_exp_level = experience_counts.idxmax()
count = experience_counts.max()

result = (
    "Чаще всего высокий рейтинг получают фрилансеры уровня: "
    + most_common_exp_level
)
result += "Количество таких фрилансеров: " + str(count)
print(result)
