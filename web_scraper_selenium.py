from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Open a CSV file for writing
with open("data.csv", mode="w", encoding="utf-8") as csv_file:
    # Start Chrome and minimize the window
    web = webdriver.Chrome()
    web.minimize_window()

    # Write header to the CSV file
    csv_file.write("Blog_Name,Blog_Likes,Blog_Date,Image_URL\n")

    # Navigate to the initial page
    web.get("https://rategain.com/blog/")

    try:
        # Attempt to find the element indicating the total number of pages
        no_of_pages = web.find_element(By.XPATH, "(//a[@class='page-numbers'])[6]")
        total_pages = int(no_of_pages.text)
    except NoSuchElementException:
        # Set a default value if page numbers are not found
        total_pages = 1

    # Loop through all pages
    for i in range(total_pages):
        try:
            # Attempt to find the elements representing blogs on the page
            no_of_blogs = web.find_elements(By.CLASS_NAME, "wrap")
            total_blogs = len(no_of_blogs)
        except NoSuchElementException:
            # Set a default value if blogs are not found
            total_blogs = 0

        # Loop through all blogs on the page
        for j in range(total_blogs):
            try:
                # Find elements within a blog and extract data
                no_of_blog = no_of_blogs[j].find_element(By.CLASS_NAME, "content")
                bname = no_of_blog.find_element(By.TAG_NAME, "a").text
                likes = no_of_blog.find_element(By.CLASS_NAME, "zilla-likes").text
                date = no_of_blog.find_element(
                    By.XPATH, f"(//div[@class='blog-detail']/div/span)[{1+j*2}]"
                ).text

                try:
                    img = no_of_blogs[j].find_element(By.CLASS_NAME, "img")
                    imga = img.find_element(By.TAG_NAME, "a")
                    img_url = imga.get_attribute("data-bg")
                except NoSuchElementException:
                    # Set a default value if the image element is not found
                    img_url = ""

                # Write data to the CSV file
                csv_file.write(f'"{bname}",{likes},"{date}",{img_url}\n')

            except NoSuchElementException:
                # Handle if any element within a blog is not found
                pass

        try:
            # Find the "next" button and navigate to the next page
            next_button = web.find_element(By.CLASS_NAME, "next")
            web.get(next_button.get_attribute("href"))
        except NoSuchElementException:
            # No more next button, exit the loop
            break

# Close the browser
web.quit()
