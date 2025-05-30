import re


def extract_numbers(text):
    # Находим все числа, включая дробные
    return list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", text)))


def compare_numbers(expected_text, actual_text, tolerance=0.05):
    expected_numbers = extract_numbers(expected_text)
    actual_numbers = extract_numbers(actual_text)

    if not expected_numbers:
        print("❌ Нет эталонных чисел для сравнения")
        return False

    results = []
    for exp_num in expected_numbers:
        found_match = False
        for act_num in actual_numbers:
            diff = abs((act_num - exp_num) / exp_num)
            if diff <= tolerance:
                print(
                    f"✅ Число {act_num} близко к эталону {exp_num} \
(разница {diff*100:.2f}%)"
                )
                found_match = True
                results.append(True)
                break
        if not found_match:
            print(f"❌ Не найдено близкого значения для {exp_num}")
            results.append(False)

    return all(results)


def exact_number_match(expected_text, actual_text):
    expected_numbers = extract_numbers(expected_text)
    actual_numbers = extract_numbers(actual_text)

    if len(expected_numbers) != len(actual_numbers):
        print("❌ Количество чисел не совпадает")
        return False

    for e, a in zip(expected_numbers, actual_numbers):
        if e != a:
            print(f"❌ Число {a} не совпадает с эталоном {e}")
            return False

    print("✅ Все числа совпадают точно")
    return True


def get_percentage_diff(expected_text, actual_text):
    expected = extract_numbers(expected_text)
    actual = extract_numbers(actual_text)

    diffs = []
    for e, a in zip(expected, actual):
        diff = abs((a - e) / e) * 100
        diffs.append(diff)
    return diffs
