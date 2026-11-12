B!IWY 20261111 Roman Belousov romanb_tsm@hotmail.com

Fetch addresses from unsent ebay orders and display phones and addresses for barcoding in Australia

Summary:
I wrote this for my ebay business [selling collectable coins](https://www.ebay.com.au/str/everycoinonline).
From Australia, but this can be adopted for any country.
I needed a list of postage addresses for outstanding orders from ebay customers and I needed them to not duplicate.
I didn't see anything online that did this.
Currently I post the output into a Libre Office file,
highlight the barcodes which are bracketed with asterixes *
set them to [3 of 9 font](https://www.barcodesinc.com/free-barcode-font/) and print.
The output looks like [this](https://github.com/every-coin-online/ebay_address_get/blob/main/label%20output%20before%20barcoding.png) and the end result that goes to printer, like [this](https://github.com/every-coin-online/ebay_address_get/blob/main/label%20output%20after%20barcoding.png).
The reason I do this, is because it saves time for me at the counter and the postal worker having to type in the address and recipient's phone and sometimes get it wrong.
Printing to PDF didn't work out and I got frustrated and ran out of time.
Perhaps someone can work out that issue for me as well as fetching etsy orders.

[EBAY DEVELOPER PROGRAM](https://developer.ebay.com/): you will need to subscribe to it and in the labyrinth of their poorly-ordered
documentation, you will find the keys, mock-ups of which are displayed in the yaml file attached to this project.
I believe that I stumbled onto a yaml generator in there somewhere, but I don't remember where. Good luck.

Requirements:
This code uses the most basic libraries.
If you struggle, please email me: romanb_tsm@hotmail.com.

Bugs:
1. phone_cleanup(ph) sometimes returns a landline, despite being designed to not do that.
problem is probably length....
2. Something sometimes returns "None" as a string (I suspect). I think this may be due to
there being a second string in the address. Just don't know. Can't be fucked fixing these as
the whole thing functions well enough to save me a lot of time.
3. Obscure, but sometimes, if a customer makes a non-tracked purchase and then subsequent tracked
purchases, my algo returns the non-tracked version without the barcodes. 1 in a hundred, but it happens.
4. Free postage is treated as standard letter and I get no barcodes. Those orders are rare, but it's a bug.

Other notes:
this can be used to get a list of items sold to adjust Odoo stock, later, see code example below, it's all there.
code reference: https://gist.github.com/hmarquardt/a48448c8b04670611761.
Etsy example:
https://stackoverflow.com/questions/61416515/how-to-use-etsy-api-credentials-to-get-and-post-data-in-python.
unable to test as API key needs approval...resolved, but didn't help.
https://www.etsy.com/developers/your-apps#.
Never got the Etsy side working, will try Claude when I have time to work this out.

