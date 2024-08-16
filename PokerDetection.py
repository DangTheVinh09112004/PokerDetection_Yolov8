import cv2
from ultralytics import YOLO
from Poker import check_hand
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Poker Detection")
    parser.add_argument("--output_video", "--o", type=str, default="Out_Video.mp4")
    parser.add_argument("--input_video", "--i", type=str, default="In_Video.mp4")
    args = parser.parse_args()
    return args

def draw_text_in_image(img, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=4):
    if "\n" not in text:
        cv2.putText(img, text, position, font, fontScale, color, thickness)
    else:
        lines = text.split("\n")
        org = 0
        for line in lines:
            cv2.putText(img, line, (position[0], position[1] + org), font, fontScale, color, thickness)
            org += 40
def test(args):
    model = YOLO("runs/detect/train/weights/best.pt")
    dictionary = {0: '10C', 1: '10D', 2: '10H', 3: '10S', 4: '2C', 5: '2D', 6: '2H', 7: '2S',
                  8: '3C', 9: '3D', 10: '3H', 11: '3S', 12: '4C', 13: '4D', 14: '4H', 15: '4S',
                  16: '5C', 17: '5D', 18: '5H', 19: '5S', 20: '6C', 21: '6D', 22: '6H', 23: '6S',
                  24: '7C', 25: '7D', 26: '7H', 27: '7S', 28: '8C', 29: '8D', 30: '8H', 31: '8S',
                  32: '9C', 33: '9D', 34: '9H', 35: '9S', 36: 'AC', 37: 'AD', 38: 'AH', 39: 'AS',
                  40: 'JC', 41: 'JD', 42: 'JH', 43: 'JS', 44: 'KC', 45: 'KD', 46: 'KH', 47: 'KS',
                  48: 'QC', 49: 'QD', 50: 'QH', 51: 'QS'}
    cap = cv2.VideoCapture(args.input_video)
    out = cv2.VideoWriter(args.output_video, cv2.VideoWriter_fourcc(*"MJPG"), int(cap.get(cv2.CAP_PROP_FPS)),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        results = model.predict(frame)
        labels = list(set([dictionary[int(x)] for r in results for x in r.boxes.cls.tolist()]))
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy().astype(int)
            scores = r.boxes.conf.cpu().numpy()

            for box, cls, score in zip(boxes, classes, scores):
                x1, y1, x2, y2 = box
                label = dictionary[cls]
                text = f"{label} {score:.1f}"

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

                cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if len(labels) > 0:
            hand_results = check_hand(labels)
    #        cv2.putText(frame, hand_results, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            draw_text_in_image(frame, hand_results, (50, 50))
        out.write(frame)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    args = get_args()
    test(args)