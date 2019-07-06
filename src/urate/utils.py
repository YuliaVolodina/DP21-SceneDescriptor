def image_to_dict(image):
	return {
		'id': image.id,
		'path': image.path,
		'caption': image.caption
	}


def rating_to_dict(rating):
	return {
		'user_id': rating.user_id,
		'image_id': rating.image_id,
		'validity': rating.validity,
		'minimalist': rating.minimalist,
		'distinct_items': rating.distinct_items,
		'details': rating.details,
		'spatial_info': rating.spatial_info
	}
