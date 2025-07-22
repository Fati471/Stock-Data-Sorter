import streamlit as st
import random
import time
import pandas as pd
import string


class StockDataCollector:
    def __init__(self, record_count=50000):
        self.record_count = record_count

    def generate_company_name(self):
 
        return ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 10)))

    def collect_data(self):
        return [
            {"Company": self.generate_company_name(), "Price": random.randint(1, 1000)}
            for _ in range(self.record_count)
        ]


def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]["Price"] < right[j]["Price"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[0]
    left = [x for x in data[1:] if x["Price"] < pivot["Price"]]
    right = [x for x in data[1:] if x["Price"] >= pivot["Price"]]
    return quick_sort(left) + [pivot] + quick_sort(right)


if "data" not in st.session_state:
    st.session_state.data = []

if "sorted_data" not in st.session_state:
    st.session_state.sorted_data = []

st.title("📈 Stock Data Sorter (Up to 50,000 Records)")


record_count = st.slider("Select number of stock records to generate", min_value=1000, max_value=50000, step=1000)


if st.button("Generate Data"):
    collector = StockDataCollector(record_count)
    st.session_state.data = collector.collect_data()
    st.success(f"✅ {record_count} stock records generated!")
    st.write("### Sample of Loaded Data (First 100 rows)")
    st.dataframe(pd.DataFrame(st.session_state.data[:100]))


sort_type = st.radio("Choose Sorting Algorithm:", ("Merge Sort", "Quick Sort"))


if st.button("Sort and Display"):
    if not st.session_state.data:
        st.warning("⚠️ Please generate data first.")
    else:
        st.info("⏳ Sorting in progress... Please wait.")

        start = time.time()
        data_copy = st.session_state.data.copy()

        if sort_type == "Merge Sort":
            sorted_data = merge_sort(data_copy)
        else:
            sorted_data = quick_sort(data_copy)

        end = time.time()

        st.session_state.sorted_data = sorted_data
        st.success(f"✅ Data sorted using {sort_type} in {end - start:.2f} seconds.")
        st.write("### Sample of Sorted Data (First 100 rows)")
        st.dataframe(pd.DataFrame(st.session_state.sorted_data[:100]))


if st.button("Clear Data"):
    st.session_state.data = []
    st.session_state.sorted_data = []
    st.info("🗑️ Data cleared.")