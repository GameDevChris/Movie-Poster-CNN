import UseCNN

# Request Genre Prediction
def GenreRequest(url):
    print("Predicting image genre...")
    output = UseCNN.Genre(url)
    print(output[0])

    try:
        output[1].show()

    except Exception as e:
        print(f"An error occured: {e}")

# Request Decade Prediction
def DecadeRequest(url):
    print("Predicting image decade...")
    output = UseCNN.Decade(url)
    print(output[0])

    try:
        output[1].show()

    except Exception as e:
        print(f"An error occured: {e}")

#Uncomment and add a url to an image
#GenreRequest("https://www.digitalartsonline.co.uk/cmsdata/slideshow/3662115/baby-driver-rory-hi-res.jpg")
#DecadeRequest("https://www.digitalartsonline.co.uk/cmsdata/slideshow/3662115/baby-driver-rory-hi-res.jpg")