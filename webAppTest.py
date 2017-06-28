####################################################################################################
###   webAppTest.py description                                                                  ###
###                                                                                              ###
###   This program tests that a user can add 5 kits via the 23andMe store website.               ###
###   It performs the following actions:                                                         ###
###      1) Visit store.23andme.com/en-us/                                                       ###
###      2) Add 5 kits and enters unique names for each kit                                      ###
###      3) Continue to the shipping page and enter a valid US shipping address and other info.  ###
###      4) Continue through the shipping verification page and                                  ###
###         verifies that the payment page is reached.                                           ###
###                                                                                              ###
###   Setup Instructions, use the following app versions:                                        ###
###       1) Python version:    2.7.10 (default, Oct 23 2015, 19:19:21)                          ###
###       2) Selenium version:  2.53.0                                                           ###
###       3) Firefox version:   46.0.1                                                           ###
###                                                                                              ###
###   Running Instuctions:                                                                       ###
###      $ python 23andMe.py                                                                     ###
###                                                                                              ###
###  Author: Stan Raichlen    [circa: 28 Jun 2017]                                               ###
###                                                                                              ###
####################################################################################################

#import pdb
#pdb.set_trace()
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
#driver = webdriver.Chrome()
driver.get('https://store.23andme.com/en-us/')
time.sleep(2)

# Create a list of 5 users
kitNames = ["Mary", "Moe", "Marty", "Mark", "Mommy"]

# Cart buttons
addHealthAncestryButton = driver.find_element_by_class_name("js-add-kit")
addAncestryButton = driver.find_element_by_class_name("js-add-ancestry-kit")

# Add 5 kits with different names
count = 0
for name in kitNames:
    addHealthAncestryButton.click()
    time.sleep(2)

    inputKitNames = driver.find_elements_by_xpath("//input[@class='js-kit-name']")
    print("The number of kit names found is " + str(len(inputKitNames)))
    message = "Incorrect number of input windows, found " + str(len(inputKitNames)) + " but expected " + str(count + 1) + "." 
    assert ( len(inputKitNames) == count + 1 ), message
    inputKitNames[count].send_keys(kitNames[count])
    time.sleep(2)
    count = count + 1

submitButton = driver.find_element_by_class_name("submit")
submitButton.click()

print ("\nOn to page 2 of the kit buying process.\n")
time.sleep(4)

print ("Begin loading the shipping address form.")

# Shipping address information
shipping = ["Stan", "Raichlen", "Benetech", "153 Waverly Place", "Mountain View",\
           "California", 94040, "stanr789@gmail.com", "650-555-1514"]

# There are 2 shipping pages that may be accessed when the initial Continue
# button is clicked, one has the first name input box id = "id_first_name", while
# the other has the first name input box id = "js-shipping-firstname".

pageID1 = driver.find_elements_by_id("id_first_name")
pageID2 = driver.find_elements_by_id("js-shipping-firstname")
shippingPageType = 0;
if (len(pageID1) == 1):
    shippingPageType = 1;
elif (len(pageID2) == 1):
    shippingPageType = 2;
assert (len(pageID1) + len(pageID2) == 1), "No shipping page detected."
print("Type " + str(shippingPageType) + " shipping page detected.")

if ( shippingPageType == 1 ):
    firstName      = driver.find_element_by_id("id_first_name")
    lastName       = driver.find_element_by_id("id_last_name")
    company        = driver.find_element_by_id("id_company")
    address        = driver.find_element_by_id("id_address")
    city           = driver.find_element_by_id("id_city")
    selectState    = Select(driver.find_element_by_id("id_state"))
    zip            = driver.find_element_by_id("id_postal_code")
    email          = driver.find_element_by_id("id_email")
    phone          = driver.find_element_by_id("id_int_phone")
    continueButton = driver.find_element_by_class_name("button-continue")
else:
    firstName      = driver.find_element_by_id("js-shipping-firstname")
    lastName       = driver.find_element_by_id("js-shipping-lastname")
    company        = driver.find_element_by_id("js-shipping-company")
    address        = driver.find_element_by_id("js-shipping-address")
    city           = driver.find_element_by_id("js-shipping-city")
    selectState    = Select(driver.find_element_by_id("js-shipping-state"))
    zip            = driver.find_element_by_name("postalCode")
    email          = driver.find_element_by_id("js-shipping-email")
    phone          = driver.find_element_by_id("js-shipping-phone")
    continueButton = driver.find_element_by_class_name("spc-next-button")

elements = [firstName, lastName, company, address, city, selectState, \
            zip, email, phone]
for i in xrange(0, len(elements)):
    if (shipping[i] == "California"):
        selectState.select_by_visible_text(shipping[i])
    else:
        elements[i].send_keys(shipping[i])
    time.sleep(2)

print("Finished loading the shipping info.")

driver.execute_script("window.scrollBy(0, -150);")
time.sleep(1)
continueButton.click()

print ("\nOn to Address Verification page (3) of the kit buying process.")
time.sleep(5)

if (shippingPageType == 1):
    # For type 1 page
    verificationButton = driver.find_element_by_class_name("button-continue")
    verificationButton.click()

    print ("On to billing page for QA test.")
    billingPage = driver.find_elements_by_id("progress-label")
    if ( len(billingPage) > 0 ):
        payment = driver.find_element_by_class_name("payment-total")
        # TODO: Verify that the payment amount is $945.35 (and why it differs from type 2)
        print("\nFinal billing page identified, TEST COMPLETED SUCCESSFULLY!")
    else:
        print("\nFinal billing page not found, TEST FAILED!")
    assert ( len(billingPage) > 0 ), "Failed to detect the Billing label for the Type 1 shipping page."

else:
    # For type 2 page
    verificationButton = driver.find_element_by_class_name("spc-verification-div-button")
    verificationButton.click()

    print ("On to billing page for QA test.")
    # TODO: determine payment link
    # TODO: Verify that the payment amount is $915.40 (and why it differs from type 1)
    billingPage = driver.find_elements_by_id("js-billing")
    if ( len(billingPage) > 0 ):
        print("\nFinal billing page identified, TEST COMPLETED SUCCESSFULLY!")
    else:
        print("\nFinal billing page not found, TEST FAILED!")
    assert ( len(billingPage) > 0 ), "Failed to detect the Billing label for the Type 2 shipping page."

exit()

####################################################################################################
####       Following are 2 sets of terminal output from running this test:                      ####
####################################################################################################
#
# [Sun Jun 28 10:56:45] stanr@2014-B-056 ~/challenge/23andMe
# $ python 23andMe.py
# The number of kit names found is 1
# The number of kit names found is 2
# The number of kit names found is 3
# The number of kit names found is 4
# The number of kit names found is 5
# 
# On to page 2 of the kit buying process.
# 
# Begin loading the shipping address form.
# Type 2 shipping page detected.          <----  NB: Type 2 shipping page
# Finished loading the shipping info.
# 
# On to Address Verification page (3) of the kit buying process.
# On to billing page for QA test.
# 
# Final billing page identified, TEST COMPLETED SUCCESSFULLY!
#
#################################
# 
# [Sun Jun 25 11:01:39] stanr@2014-B-056 ~/challenge/23andMe
# $ python 23andMe.py
# The number of kit names found is 1
# The number of kit names found is 2
# The number of kit names found is 3
# The number of kit names found is 4
# The number of kit names found is 5
# 
# On to page 2 of the kit buying process.
# 
# Begin loading the shipping address form.
# Type 1 shipping page detected.          <----  NB: Type 1 shipping page
# Finished loading the shipping info.
# 
# On to Address Verification page (3) of the kit buying process.
# On to billing page for QA test.
#
# Final billing page identified, TEST COMPLETED SUCCESSFULLY!

#### the end #######################################################################################
