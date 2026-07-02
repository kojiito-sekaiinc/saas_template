def test_home_page(page):

    page.goto(
        "http://localhost:8000"
    )

    assert page.title() != ""