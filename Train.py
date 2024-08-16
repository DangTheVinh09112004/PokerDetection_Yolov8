from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model.train(data="/home/vinhdeptrai/PycharmProjects/pythonProject/pythonproject2/PlayingCards/data.yaml",
                      epochs=100, imgsz=640)
