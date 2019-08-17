"""Main entry point."""
import json
from os import listdir
from sys import argv


def read_json(directory, filename):
    print(f"Reading {filename}")
    file_path = f"{directory}\\{filename}"
    content = open(file_path, "r", encoding="utf-8").readlines()
    merged = ""
    for line in content:
        merged += line

    return json.loads(merged)


def build_transaction(raw_json):
    transaction = {}
    if "transactionMerchant" in raw_json.keys():
        transaction["merchant_name"] = raw_json["transactionMerchant"]["name"]
    else:
        transaction["merchant_name"] = "No name given"
    products = []
    for product in raw_json["lineItem"]:
        name = get_product_name(product)
        price = get_product_price(product)
        products.append({"name": name,
                         "price": price})
    transaction["products"] = products

    return transaction


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
    loops = 0
    for filename in listdir(argv[1]):
        loops += 1
        content_json = read_json(argv[1], filename)

        transaction = build_transaction(content_json)

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
    print(f"{loops}")
    print(merchants)
