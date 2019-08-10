import json
from os import listdir
from sys import argv


def get_product_name(product):
    if "name" in product.keys():
        product_name = product["name"]
    elif "productInfo" in product["purchase"].keys():
        product_name = product["purchase"]["productInfo"]["name"]
    else:
        product_name = "No name given"
    return product_name


def get_product_price(product):
    if "purchase" in product.keys():
        if "unitPrice" in product["purchase"].keys():
            price = product["purchase"]["unitPrice"]["amountMicros"]
            price = price.replace("0000", "")
            price = int(price)
            price = price / 100
        else:
            price = None
    else:
        price = None
    return price


if __name__ == "__main__":
    if not len(argv) == 2:
        print("Too many arguments")
        exit(1)

    merchants = {}
    for filename in listdir(argv[1]):
        print(f"Reading {filename}")
        content = open(argv[1] + "\\" + filename, "r", encoding="utf-8").readlines()
        merged = ""
        for line in content:
            merged += line

        content_json = json.loads(merged)

        transaction = {}
        if "transactionMerchant" in content_json.keys():
            transaction["merchant_name"] = content_json["transactionMerchant"]["name"]
        else:
            transaction["merchant_name"] = "No name given"
        products = []
        for product in content_json["lineItem"]:
            name = get_product_name(product)
            price = get_product_price(product)
            products.append({"name": name,
                             "price": price})
        transaction["products"] = products

        if transaction["merchant_name"] in merchants:
            merchants[transaction["merchant_name"]] += 1
        else:
            merchants[transaction["merchant_name"]] = 1

        merc = transaction["merchant_name"]
        print(f"{merc}:")
        for product in transaction["products"]:
            name = product["name"]
            price = product["price"]
            print(f"\t{name} - {price}")
    print(merchants)
