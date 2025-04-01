from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app, get_db
from ..database import Base

# Используем тестовую базу данных в памяти
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_module(module):
    # Создаем таблицы в тестовой базе данных перед запуском тестов
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    # Удаляем таблицы после завершения всех тестов
    Base.metadata.drop_all(bind=engine)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в магазин комплектующих!"}


def test_create_videocard():
    response = client.post(
        "/videocards/",
        json={"name": "RTX 3090", "manufacturer": "Nvidia", "memory": 24, "price": 1500.00, "description": "Топовая видеокарта"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "RTX 3090"
    assert data["manufacturer"] == "Nvidia"
    assert data["memory"] == 24
    assert data["price"] == 1500.00
    assert data["description"] == "Топовая видеокарта"
    assert "id" in data
    videocard_id = data["id"]

    # Проверяем, что видеокарта действительно создалась и её можно прочитать
    response = client.get(f"/videocards/{videocard_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "RTX 3090"


def test_read_videocards():
    # Сначала создадим несколько видеокарт для тестирования
    client.post(
        "/videocards/",
        json={"name": "RTX 3080", "manufacturer": "Nvidia", "memory": 10, "price": 800.00, "description": "Отличная видеокарта"},
    )
    client.post(
        "/videocards/",
        json={"name": "RX 6800 XT", "manufacturer": "AMD", "memory": 16, "price": 750.00, "description": "Конкурент Nvidia"},
    )

    response = client.get("/videocards/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Учитываем, что в предыдущем тесте мы уже создали одну видеокарту
    assert data[0]["manufacturer"] == "Nvidia"
    assert data[1]["manufacturer"] == "Nvidia"  # Добавлено для уверенности

def test_read_videocard():
    # Сначала создадим видеокарту, чтобы потом её прочитать
    response = client.post(
        "/videocards/",
        json={"name": "RTX 3070", "manufacturer": "Nvidia", "memory": 8, "price": 600.00, "description": "Хорошая видеокарта"},
    )
    assert response.status_code == 200
    data = response.json()
    videocard_id = data["id"]

    response = client.get(f"/videocards/{videocard_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "RTX 3070"
    assert data["manufacturer"] == "Nvidia"


def test_create_cpu():
    response = client.post(
        "/cpus/",
        json={"name": "Ryzen 9 5900X", "manufacturer": "AMD", "cores": 12, "clock_speed": 3.7, "price": 550.00, "description": "Мощный процессор"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Ryzen 9 5900X"
    assert data["manufacturer"] == "AMD"
    assert data["cores"] == 12
    assert data["clock_speed"] == 3.7
    assert data["price"] == 550.00
    assert data["description"] == "Мощный процессор"
    assert "id" in data
    cpu_id = data["id"]

    # Проверяем, что процессор действительно создался, и его можно прочитать
    response = client.get(f"/cpus/{cpu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ryzen 9 5900X"

def test_read_cpus():
    client.post(
        "/cpus/",
        json={"name": "i7-10700K", "manufacturer": "Intel", "cores": 8, "clock_speed": 3.8, "price": 350.00, "description": "Процессор Intel"},
    )

    response = client.get("/cpus/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["manufacturer"] == "AMD" # First CPU is 5900X, from the previous test
    assert data[1]["manufacturer"] == "Intel"

def test_read_cpu():
    response = client.post(
        "/cpus/",
        json={"name": "i5-11600K", "manufacturer": "Intel", "cores": 6, "clock_speed": 3.9, "price": 250.00, "description": "Процессор Intel"},
    )
    assert response.status_code == 200
    data = response.json()
    cpu_id = data["id"]

    response = client.get(f"/cpus/{cpu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "i5-11600K"
    assert data["manufacturer"] == "Intel"