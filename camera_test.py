import cv2
# Note the following is the typical rtsp url for streaming from an ip cam
# source = "rtsp://user:password@ipaddress:port/<camera specific stuff>"
# Each manufacturer is different. For my alibi cameras, this would be
# a valid url to use with the info you provided.
source = "rtsp://admin:autogruppe4@192.168.0.101//Streaming/Channels/1"
cap = cv2.VideoCapture(source)

ok_flag = True
print("over while")
while ok_flag:
    print('in while')
    (ok_flag, img) = cap.read()
    if not ok_flag:
        print
        break
    print(img)

    cv2.imshow("some window", img)
    if cv2.waitKey(10) == 27:
        break
print('under while')
cv2.destroyAllWindows()
