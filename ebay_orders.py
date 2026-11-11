# B!IWY 20261111 Roman Belousov romanb_tsm@hotmail.com
# return addresses for outstanding ebay orders
#
# |=========================================================================================================
# | Summary:
# | I wrote this for my ebay business selling collectable coins https://www.ebay.com.au/str/everycoinonline
# | From Australia, but this can be adopted for any country.
# | I needed a list of postage addresses for outstanding orders from ebay customers
# | And I needed them to not duplicate
# | I didn't see anything online that did this
# | Currently I post the output into a Libre Office file,
# | highlight the barcodes which are bracketed with asterixes *
# | set them to 3 of 9 font https://www.barcodesinc.com/free-barcode-font/ and print
# | The reason I do this, is because it saves time for me at the counter and
# | the postal worker having to type in the address and recipient's phone
# | and sometimes get it wrong.
# | Printing to PDF didn't work out and I got frustrated and ran out of time
# | perhaps someone can work out that issue for me as well as fetching etsy orders
# | EBAY DEVELOPER PROGRAM: you will need to subscribe to it and in the labyrinth of their poorly-ordered
# | documentation, you will find the keys that are displayed in the yaml file attached to this project
# | I believe that I stumbled onto a yaml generator in there somewhere, but I don't remember where. Good luck.
# |=========================================================================================================
#
# |=========================================================================================================
# | Requirements:
# | This code uses the most basic libraries.
# | If you struggle, please email me: romanb_tsm@hotmail.com.
# |=========================================================================================================
#
# |=========================================================================================================
# | Bugs:
# | 1. phone_cleanup(ph) sometimes returns a landline, despite being designed to not do that.
# | problem is probably length....
# | 2. Something sometimes returns "None" as a string (I suspect). I think this may be due to
# | there being a second string in the address. Just don't know. Can't be fucked fixing these as
# | the whole thing functions well enough to save me a lot of time.
# | 3. Obscure, but sometimes, if a customer makes a non-tracked purchase and then subsequent tracked
# | purchases, my algo returns the non-tracked version without the barcodes. 1 in a hundred, but it happens.
# |=========================================================================================================
#
# |=========================================================================================================
# | Other notes:
# | this can be used to get a list of items sold to adjust Odoo stock, later, see code example below, it's all there
# | code reference: https://gist.github.com/hmarquardt/a48448c8b04670611761
# | Etsy example:
# | https://stackoverflow.com/questions/61416515/how-to-use-etsy-api-credentials-to-get-and-post-data-in-python
# | unable to test as API key needs approval...resolved, but didn't help
# | https://www.etsy.com/developers/your-apps#
# | Never got the Etsy side working, will try Claude when I have time to work this out
# |=========================================================================================================

from ebaysdk.trading import Connection as trading
from datetime import datetime, timedelta
import xmltodict, pprint, re, lxml.html
import string

def phone_cleanup(ph) :
    # removes landlines, adds 0 to mobile numbers not beginning with a zero
    if len(ph) == 9 and ph[0] == '4' :
        return('0'+ph)
    else :
        #ignore Australian landlines, which begin with 02, 03, 07 & 08
        if len(ph) == 10 and ph[1] in '2378' :
            return(None)
    #I should really remove spaces here, but the Ebay API doesn't seem to return spaces...I think
    return(ph)

def state_cleanup(st) :
    #replaces non-abbreviated spellings of Australian states with laconic acronyms
    st = rem_punct(st)

    dict = {'western australia': 'WA',
            'victoria': 'VIC',
            'new south wales': 'NSW',
            'south australia': 'SA',
            'northern territory': 'NT',
            'queensland': 'QLD',
            'tasmania': 'TAS'}
    return (dict.get(st.lower(),st))

def rem_punct (s) :
    # removes punctuation marks from text
    return s.translate(str.maketrans('', '', string.punctuation))

# ebay section:

api = trading(config_file='ebay.yaml')

#I've tightened the daterange to 15 days from now. I was getting an issue with pagination and rather than deal with pagination, just tightened the start-finish window as I should have done before anyway
#anyone with more than 100 orders in 15 days will need to introduce pagination

start_date = datetime.now() - timedelta(days=15)
#start_date = str(datetime.now().year)+'-'+str(datetime.now().month-1).rjust(2,'0')+'-01T00:00:00.005Z'

end_date = str(datetime.now().year)+'-'+str(datetime.now().month).rjust(2,'0')+'-'+str(datetime.now().day+1).rjust(2,'0')+'T00:00:00.005Z'

print(start_date)
print(end_date)

response = api.execute('GetOrders', {'CreateTimeFrom': start_date, 'CreateTimeTo': end_date, 'DetailLevel': 'ReturnAll', 'OrderStatus': 'Completed'})

# left in for debugging purposes:
#response = api.execute('GetOrders', {'CreateTimeFrom': start_date, 'CreateTimeTo': end_date, 'DetailLevel': 'ReturnAll'})

orders = xmltodict.parse(response.content)

#for debugging:

#print(orders)

#exit()

names = [] # quick and nasty to check for duplicate addresses by storing the name only
# doesn't work if postage is not combined and the first instance of the same address is for a standard letter. I mean it works, but doesn't return the barcode(s). Oh well. Minor isssue until I can be stuffed looking at it.
for order in orders['GetOrdersResponse']['OrderArray']['Order']:
    #leaving this debug code in, in case I need to look at the data I'm dealing with again

    #if order['OrderID'] = 25-13568-78447
    #print('\n- - - Record begins - - - OrderID: '+' '+order['OrderID']+'\n')
    #if order['OrderID'] == '01-13900-87734' :
    #    pprint.pprint(order)


    #only return addresses for orders that don't have a shipping date, are not cancelled and are for Australia
    if ('ShippedTime' not in order and order['ShippingAddress']['Country'] == 'AU' and order['ShippingAddress']['Name'] not in names and not(order['OrderStatus'] == 'Cancelled')):
        #print('OrderID: '+' '+order['OrderID']+' '+'OrderStatus: '+' '+order['OrderStatus']+' ')

        ph = ''

        names.append(order['ShippingAddress']['Name'])

        # do not print barcodes for landline phones or orders with standard untracked packaging
        ph = (phone_cleanup(order['ShippingAddress']['Phone']))
        if ph is not None and not order['ShippingServiceSelected']['ShippingService'] == 'AU_AusPostStandardLetter' :
            print('*'+ph+'*')
            print(ph)

        print(order['ShippingAddress']['Name'].title())
        if "ebay:" not in order['ShippingAddress']['Street1']:
            print(order['ShippingAddress']['Street1'])
        print(order['ShippingAddress']['Street2'])

        #no need for suburb & postalcode barcodes for standard letters, yes yes I know redundant branch, but easier to read
        if order['ShippingServiceSelected']['ShippingService'] == 'AU_AusPostStandardLetter' :
            print(rem_punct(order['ShippingAddress']['CityName'])+' '+state_cleanup(order['ShippingAddress']['StateOrProvince'])+' '+order['ShippingAddress']['PostalCode']+'\n')
        else :
            print(rem_punct(order['ShippingAddress']['CityName'])+' '+state_cleanup(order['ShippingAddress']['StateOrProvince'])+' '+order['ShippingAddress']['PostalCode'])
            #there is an issue encoding a space for 3 of 9. '!' works for Libre Office on my particular setup, other suggestions were to substitute '_', '-', '=', or '~' - if it's not working for you, <- test those.
            print('*'+ rem_punct(order['ShippingAddress']['CityName']).upper().replace(' ','!')+'!'+order['ShippingAddress']['PostalCode']+'*\n')

#B!IWY="But! It Worked Yesterday." If I could have a dime for every time I heard that on the phone...
