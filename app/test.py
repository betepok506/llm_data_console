import pandas as pd
PATH_TO_DATA = "./data/freelancer_earnings_bd.csv"
df = pd.read_csv(PATH_TO_DATA)

# Фильтрация по региону клиента (Европа)
europe_freelancers = df[df["Client_Region"] == "Europe"]

# Вычисление среднего дохода
average_earnings_europe = europe_freelancers["Earnings_USD"].mean()

result = f"Средний доход фрилансеров с клиентами из Европы: " + "{:.2f}".format(average_earnings_europe) + " USD"

print(result)