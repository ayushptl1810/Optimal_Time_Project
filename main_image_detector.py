import OcrToTableTool as ottt
import TableExtractor as te
import TableLinesRemover as tlr
import cv2

def process_image(path_to_image):
    print(path_to_image)
    table_extractor = te.TableExtractor(path_to_image)
    perspective_corrected_image = table_extractor.execute()
    # cv2.imshow("perspective_corrected_image", perspective_corrected_image)


    lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
    image_without_lines = lines_remover.execute()
    # cv2.imshow("image_without_lines", image_without_lines)

    ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image)
    filename = ocr_tool.execute()

    # cv2.waitKey(10000)
    # cv2.destroyAllWindows()

    return filename

