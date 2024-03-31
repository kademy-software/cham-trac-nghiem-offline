''' 
GHI CHÚ CHƯƠNG TRÌNH 
Tác giả : Lê Tuấn Kiệt                  Đồng tác giả : Không 
Bản quyền / Giấy phép : MIT (Kademy Software)
Mã nguồn mở? : Có, mọi người đều có thể sử dụng mã nguồn này 
Mục đích chương trình : Nghiên cứu 
Thư viện sử dụng : numpy, cv2 
Ngôn ngữ lập trình : Python 

DANH SÁCH THUẬT NGỮ 
countours: Các viền, là các vùng hình chữ nhật của phiếu chấm trắc nghiệm
DANH SÁCH BIẾN, HÀM SỬ DỤNG 
1. Hàm rectCountour(countours) :Lấy hình chữ nhật lớn nhất 
'''
import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
def rectCountour(countours): 
    rectCon=[]
    for i in countours:
        area=cv2.contourArea(i)
        #print(area)
        if area>50: 
            peri=cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            #print("Điểm gốc:",len(approx))
            if len(approx)==4:
                rectCon.append(i)
    rectCon= sorted(rectCon,key=cv2.contourArea,reverse=True)
    return rectCon 
            
        
        
        
def getContours(img):
    imgContour = img.copy()  # Initialize imgContour within the function
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3:
                objectType = "Tri"
            elif objCor == 4:
                aspRatio = w / float(h)
                if 0.98 < aspRatio < 1.03:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                objectType = "Circles"
            else:
                objectType = "None"

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX,
                        0.7, (0, 0, 0), 2)

    return imgContour  # Return the modified imgContour

# xử lý ảnh phiếu trắc nghiệm
path = 'phieu.JPG'
img = cv2.imread(path)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
imgContour = img.copy()

#Tìm viền phiếu chấm 
countours, hierarchy= cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContour,countours,-1,(0,255,0),10) 

#Tìm hình chữ nhật 
rectCon=rectCountour(countours)
biggestContour= rectCon[0]
print("Khung lớn nhất:",len(biggestContour))

#In phiếu kết quả
imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8, ([img, imgGray, imgBlur,imgCanny],
                             [imgContour, imgBlank,imgBlank,imgBlank])) 

cv2.imshow("Phieu cham THPT Tinh Bien", imgStack)
cv2.waitKey(0)
