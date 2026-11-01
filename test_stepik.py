import math
import time

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize("link", [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1",
])
def test_stepik_feedback(browser, link):

    wait = WebDriverWait(browser, 30)

    print(f"\nОткрываем страницу: {link}")
    browser.get(link)

    # Ждём загрузки задания
    wait.until(
        lambda driver: (
            (wrappers := driver.find_elements(
                By.CSS_SELECTOR, ".attempt-wrapper"
            ))
            and wrappers[0].get_attribute("data-quiz-state") != "loading"
        )
    )

    wrapper = browser.find_element(
        By.CSS_SELECTOR, ".attempt-wrapper"
    )

    state = wrapper.get_attribute("data-quiz-state")

    print("Текущее состояние задания:", state)

    # Если задание уже решено, начинаем заново
    if state == "correct":

        restart_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.attempt-wrapper-button")
            )
        )

        restart_button.click()

        print("Нажали «Начать сначала»")

    # Ждём доступного поля
    answer_input = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "textarea.string-quiz__textarea")
        )
    )

    print("Поле ответа доступно")

    # Вычисляем и вводим ответ
    answer = math.log(int(time.time()))

    answer_input.send_keys(str(answer))

    print("Ввели ответ:", answer)

    # Отправляем ответ
    submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.attempt-wrapper-button")
        )
    )

    submit_button.click()

    print("Ответ отправлен")

    # Ждём завершения проверки ответа
    wait.until(
        lambda driver: (
            (wrappers := driver.find_elements(
                By.CSS_SELECTOR, ".attempt-wrapper"
            ))
            and wrappers[0].get_attribute("data-quiz-state")
            in ("correct", "wrong", "partially_correct")
        )
    )

    wrapper = browser.find_element(
        By.CSS_SELECTOR, ".attempt-wrapper"
    )

    print("\n========== РЕЗУЛЬТАТ ПРОВЕРКИ ==========")

    print(
        "Состояние задания:",
        wrapper.get_attribute("data-quiz-state")
    )

    print("\nСтатус submission-show:")

    submissions = wrapper.find_elements(
        By.CSS_SELECTOR, ".submission-show"
    )

    for submission in submissions:
        print(
            "data-status:",
            submission.get_attribute("data-status")
        )
        print(
            "data-quiz-state:",
            submission.get_attribute("data-quiz-state")
        )

    print("\nВсе найденные подсказки:")

    hints = wrapper.find_elements(
        By.CSS_SELECTOR, ".smart-hints__hint"
    )

    all_feedback = []

    for hint in hints:
        if hint.is_displayed():
            text = hint.text.strip()
            all_feedback.append(text)
            print("Подсказка:", repr(text))

    print("\nСообщения о результате:")

    messages = wrapper.find_elements(
        By.CSS_SELECTOR, ".attempt-wrapper-message__item"
    )

    for message in messages:
        if message.is_displayed():
            print("Сообщение:", repr(message.text.strip()))

    print("\nПолный текст блока результата:")

    result_blocks = wrapper.find_elements(
        By.CSS_SELECTOR, ".submission-show"
    )

    for block in result_blocks:
        print(block.text)

    print("========== КОНЕЦ РЕЗУЛЬТАТА ==========\n")

    # Строго проверяем текст фидбека
    actual_feedback = "\n".join(all_feedback)

    assert actual_feedback == "Correct!", (
        f"Страница: {link}. "
        f"Полученный фидбек: {actual_feedback!r}. "
        f"Состояние задания: "
        f"{wrapper.get_attribute('data-quiz-state')}"
    )