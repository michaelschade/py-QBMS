#
# Created by: Michael Schade, 2009.
# Website: www.maschade.com/os/qbms
# Please retain this notice and any attribution
# when using this code. It is not intended to be
# removed.
#
# Please note that this is an incomplete,
# albeit in my tests functional, Python
# implementation of Intuit's QBMS API.
# I am in no way affiliated with Intuit,
# but saw a need in a recent project
# for integration. After seeing how
# their API functioned, it seemed reasonable
# enough to release it to the open source community.
#
# Although I have read through all of Intuit's
# relevant documentation regarding their API
# and the security associated with it, it
# is necessary to understand that simply
# importing this API does not guarantee
# security when processing credit cards.
# I urge, for the sake of security as a whole,
# that you read through Intuit's documentation
# as well. It does not hurt to broaden your scope
# of understanding on how the backend works. This
# is meant as a convenience, not as a replacement
# for knowledge.
#
# Use at your own risk. As time progresses,
# I will try to add more to allow the API
# to properly complete the qbms spec.
#

BASE_URL = "webmerchantaccount.quickbooks.com"
TRANSACTION_URL = "https://webmerchantaccount.quickbooks.com/j/AppGateway/"

try: from lxml import etree
except ImportError:
    print "Fatal error: dependency issue for lxml. Operation aborted."
    quit()

class QBMS():
    VISA            = 'Visa'
    MASTERCARD      = 'MasterCard'
    DISCOVER        = 'Discover'
    AMERICANEXPRESS = 'AmericanExpress'
    JCB             = 'JCB'
    DINERSCLUB      = 'DinersClub'
    
    def __init__(self, appID, appLogin, connectionTicket, certificateFile, keyFile):
        self.appID              = appID
        self.appLogin           = appLogin
        self.connectionTicket   = connectionTicket
        self.certificateFile    = certificateFile
        self.keyFile            = keyFile
    
    def __getDateTime(self):
        from datetime import datetime
        return datetime.isoformat(datetime.now())[:-7]
    
    def __submitRequest(self, xmlData):
        baseRequest = '<?xml version="1.0"?><?qbmsxml version="3.0"?>'
        postData = baseRequest + etree.tostring(xmlData)
        postData = postData.strip('\n \t') # Must be sanitized before POSTing.
        try: from httplib import HTTPSConnection
        except ImportError:
            print "Fatal error: importing dependency for an HTTPS connection."
        https = HTTPSConnection(BASE_URL, 443, self.keyFile, self.certificateFile)
        from socket import error as socketError
        try:
            https.request("POST", TRANSACTION_URL, postData, {
                'Content-type': 'application/x-qbmsxml',
                'Content-length': len(postData),
            })
        except socketError:
            print "Fatal error: problem communicating with Intuit's servers."
            quit()
        response = https.getresponse().read()
        https.close()
        return response
    
    def __sessionRequest(self):
        qbmsxml = etree.Element("QBMSXML")
        qbmsxml.append(etree.Element("SignonMsgsRq"))
        cardRequest = etree.SubElement(qbmsxml[0], "SignonAppCertRq")
        etree.SubElement(cardRequest, "ClientDateTime").text    = self.__getDateTime()
        etree.SubElement(cardRequest, "ApplicationLogin").text  = self.appLogin
        etree.SubElement(cardRequest, "ConnectionTicket").text  = self.connectionTicket
        etree.SubElement(cardRequest, "Language").text          = "English"
        etree.SubElement(cardRequest, "AppID").text             = self.appID
        etree.SubElement(cardRequest, "AppVer").text            = "1.0"
        self.sessionID = etree.fromstring(self.__submitRequest(qbmsxml))[0][0].find("SessionTicket").text
    
    def __errorCheck(self, xml):
        # If a string, convert it to an XML object.
        if type(xml) == str:
            try:
                xml = etree.fromstring(xml)
            except etree.XMLSyntaxError:
                print "Fatal error: return data malformed."
                return True
        statusCode = xml[1][0].get("statusCode")
        from qbmsError import QBMSException, QBMS_EXCEPTIONS
        if statusCode in QBMS_EXCEPTIONS:
            QBMSException().raiseError(statusCode)
    
    def __buildActionRequest(self):
        try: self.sessionID
        except: self.__sessionRequest()
        qbmsxml = etree.Element("QBMSXML")
        qbmsxml.append(etree.Element("SignonMsgsRq"))
        signonTicket = etree.SubElement(qbmsxml[0], "SignonTicketRq")
        signonTicket.append(etree.Element("ClientDateTime"))
        signonTicket[0].text = self.__getDateTime()
        signonTicket.append(etree.Element("SessionTicket"))
        signonTicket[1].text = self.sessionID
        # Credit Card Auth
        qbmsxml.append(etree.Element("QBMSXMLMsgsRq"))
        return qbmsxml
    
    def __genTransID(self):
        try:
            from uuid import uuid1
            return str(uuid1())
        except ImportError:
            print "Failed to import uuid. Trying datetime."
            try:
                from datetime import datetime
                return str(datetime.now())
            except ImportError:
                print "Fatail error: attempt at importing datetime failed."
                quit()
    
    def voidOrRefundCard(self, ccTransID, amount=0, salesTax=0, forceRefund=False, transID=""):
        qbmsxml = self.__buildActionRequest()
        cardRequest = etree.SubElement(qbmsxml[1], "CustomerCreditCardTxnVoidOrRefundRq")
        if transID == "": transID = self.__genTransID()
        etree.SubElement(cardRequest, "TransRequestID").text = str(transID)[:50]
        etree.SubElement(cardRequest, "CreditCardTransID").text = str(ccTransID)[:12]
        if amount != "": etree.SubElement(cardRequest, "Amount").text = "%0.2f" % amount
        # CommercialCardCode
        if salesTax != "": etree.SubElement(cardRequest, "SalesTaxAmount").text = "%0.2f" % salesTax
        if forceRefund: etree.SubElement(cardRequest, "ForceRefund").text = "True"
        # BatchID
        response = self.__submitRequest(qbmsxml)
        self.__errorCheck(response)
        return response # Response returned as a string. Convert to XML first?
    
    def chargeCard(self, ccNumber, expMonth, expYear, amount, ccCode="", ccName="", ccAddress="", ccZip="", transID="", salesTax="", cardPresent=False, 
eCommerce=True, recurring=False):
        qbmsxml = self.__buildActionRequest()
        cardRequest = etree.SubElement(qbmsxml[1], "CustomerCreditCardChargeRq")
        if transID == "": transID = self.__genTransID()
        etree.SubElement(cardRequest, "TransRequestID").text = str(transID)[:50]
        etree.SubElement(cardRequest, "CreditCardNumber").text = str(ccNumber)[:19]
        etree.SubElement(cardRequest, "ExpirationMonth").text = str(expMonth)
        etree.SubElement(cardRequest, "ExpirationYear").text = str(expYear)
        if recurring: etree.SubElement(cardRequest, "IsRecurring").text = repr(recurring)
        elif cardPresent: etree.SubElement(cardRequest, "IsCardPresent").text = repr(cardPresent)
        elif eCommerce: etree.SubElement(cardRequest, "IsECommerce").text = repr(eCommerce)
        # Track2Data[:39]
        etree.SubElement(cardRequest, "Amount").text = "%0.2f" % amount
        if ccName != "": etree.SubElement(cardRequest, "NameOnCard").text = str(ccName)[:30]
        if ccAddress != "": etree.SubElement(cardRequest, "CreditCardAddress").text = str(ccAddress)[:30]
        if ccZip != "": etree.SubElement(cardRequest, "CreditCardPostalCode").text = str(ccZip)[:9]
        # CommercialCardCode[:25]
        if salesTax != "": etree.SubElement(cardRequest, "SalesTaxAmount").text = str(salesTax)
        if ccCode != "": etree.SubElement(cardRequest, "CardSecurityCode").text = str(ccCode)[:4]
        response = self.__submitRequest(qbmsxml)
        self.__errorCheck(response)
        return response # Response returned as a string. Convert to XML first?

