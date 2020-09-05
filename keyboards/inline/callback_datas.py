from aiogram.utils.callback_data import CallbackData

ChoiceBrandCallback = CallbackData('brand', 'brand_name', 'pk')
ChoiceModelCallback = CallbackData('model', 'model_name', 'pk')
CarsListCallback = CallbackData('cars_list', 'brand_pk', 'model_pk', 'page')
CarDetailCallback = CallbackData('car_detail', 'car_pk', 'brand_pk', 'model_pk', 'page')
MyCarDetailCallback = CallbackData('my_car_detail', 'car_pk', 'page')
MyCarsListCallback = CallbackData('my_cars_list', 'page')
UpdateCarCallback = CallbackData('car_upd', 'field', 'pk', 'page')
ImageArrowsCallback = CallbackData('img_arrow', 'img_idx')
ImageCallback = CallbackData('img', 'img_id')
