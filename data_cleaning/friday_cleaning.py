import pandas as pd

df = pd.read_excel("friday_data.xlsx")
#print(df)

#DROP COLUMNS
df = df.drop(columns=["Unnamed: 0", "Transaction ID", "Transaction Type", "Till ID"])
#REMOVE THE FIRST ROW
df = df.drop([0])
#REMOVE ANY DUPLICATES
df = df.drop_duplicates()
#REMOVE ANY NaN VALUES
df = df.dropna(how="any")
#RESET THE INDEX
df = df.reset_index(drop=True)
#RESET INDEX TO START AT 1 INSTEAD OF 0
df.index += 1
#CONVERT VALUE TO INTEGERS
df["Total Items"] = df["Total Items"].astype(int)

print(df)

#DIFFERENT PAYMENT METHODS USED
print(df["Payment Method"].value_counts())

#TOTAL INCOME FROM COST COLUMN
total_income = df["Cost"].sum()
print("Total Income:", total_income)

#THE HIGHEST SPEND
highest_spend = df["Cost"].max()
print("Highest Spend:", highest_spend)

#THE MOST VALUED STAFF MEMBER
most_common_staff_member = df["Staff"].value_counts().idxmax()
most_common_staff_member_count = df["Staff"].value_counts().max()
print("Most Common Staff Member:", most_common_staff_member)
print("Number of Times on Till:", most_common_staff_member_count)

def remove_punctuation(basket):
    basket = str(basket)
    basket = basket.replace("[", "")
    basket = basket.replace("]", "")
    basket = basket.replace("'", "")
    return basket

df["Basket"] = df["Basket"].apply(remove_punctuation)

def split_basket(basket_str):
    elements = basket_str.split(", ")
    return [item.strip() for item in elements]

df["Basket"] = df["Basket"].apply(split_basket)

print(df["Basket"])

df = df.explode("Basket", ignore_index=False)

print(df["Basket"].value_counts())

print(df.describe())

#BEST SELLING ITEM
best_selling_item = df["Basket"].value_counts().idxmax()
print("Best Selling Item:", best_selling_item)

#WORST SELLING ITEM
worst_selling_item = df["Basket"].value_counts().idxmin()
print("Worst Selling Item:", worst_selling_item)