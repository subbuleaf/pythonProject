from api_services import Business, JwtGeneration, Form1099NEC
from flask import Flask, render_template, request
import json
from core.Form1099NecList import Form1099NecList
from core.GetBusinssList import BusinessListRequest
from core.GetNecListRequest import GetNecListRequest
from core.RecipientModel import RecipientModel

appInstance = Flask(__name__)
global jwtToken


@appInstance.route('/')
def index():
    return render_template('index.html')


@appInstance.route('/createbusiness', methods=['get'])
def loadCreateBusiness():
    return render_template('createbusiness.html')


# Create Form 1099 NEC
@appInstance.route('/createForm1099NEC', methods=['get'])
def loadCreateForm1099NEC():
    return render_template('create_form_1099_nec.html')


@appInstance.route('/success', methods=['POST'])
def submit():
    input_request_json = request.form.to_dict(flat=False)

    print(input_request_json)

    response = create_business(input_request_json)

    print(response)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>BusinessId =' +
                                        response[
                                            'BusinessId'], ErrorMessage=' Business Created Successfully')

    elif 'Errors' in response and response['Errors'] is not None:

        return render_template('error_list.html', errorList=response['Errors'], status=str(response['StatusCode'])+" - "+str(response['StatusName'])+" - "+str(response['StatusMessage']))
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


@appInstance.route('/create1099nec', methods=['POST'])
def submitCreateForm1099NEC():
    input_request_json = request.form.to_dict(flat=False)

    print(input_request_json)

    businessId = ''

    if 'business_list' in input_request_json:
        businessId = input_request_json['business_list'][0]

    rName = ''
    if 'rName' in input_request_json:
        rName = input_request_json['rName'][0]

    rTIN = ''
    if 'rTIN' in input_request_json:
        rTIN = input_request_json['rTIN'][0]

    amount = ''
    if 'amount' in input_request_json:
        amount = input_request_json['amount'][0]

    recipientId = None
    if 'recipientsDropDown' in input_request_json:
        recipientId = input_request_json['recipientsDropDown'][0]

    response = create_form1099_nec(businessId, recipientId, rName, rTIN, amount)

    print(response)

    if response['StatusCode'] == 200:

        return render_template('success.html',
                               response='StatusMessage=' + response['StatusMessage'] + '<br>SubmissionId =' +
                                        response['SubmissionId'], ErrorMessage=' Form 1099NEC Created Successfully')

    elif 'Errors' in response and response['Errors'] is not None:

        return render_template('error_list.html', errorList=response['Errors'], status=str(response['StatusCode'])+" - "+str(response['StatusName'])+" - "+str(response['StatusMessage']))
    else:

        return render_template('success.html', response='StatusMessage=' + str(response['StatusCode']),
                               ErrorMessage='Message=' + json.dumps(response))


@appInstance.route('/detail', methods=['GET'])
def get_business():
    business_id = request.args.get('business_id')
    ein = request.args.get('ein')
    print(business_id)
    print(ein)
    response = get_business_detail_api(business_id, ein)
    return render_template('detail.html', response=response)


@appInstance.route('/businesslist/', methods=['GET'])
def users():

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(20)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    print(businesses)

    print(businesses[0]['BusinessId'])

    return render_template('business_list.html', businesses=businesses)


def create_business(requestJson):
    response = Business.create(requestJson)
    return response


def create_form1099_nec(businessId, recipientId, rName, rTIN, amount):
    response = Form1099NEC.create(businessId, recipientId, rName, rTIN, amount)
    return response.json()


def get_business_detail_api(businessId, einOrSSN):
    return Business.get_business_detail(businessId, einOrSSN)


@appInstance.route('/ReadBusinessList', methods=['GET'])
def get_businessList():

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(20)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    print(businesses)

    return render_template('create_form_1099_nec.html', businesses=businesses)


# on selecting business from drop down this method gets invoked
@appInstance.route('/readRecipientsList', methods=['POST'])
def readRecipientsList():
    selectedBusiness = request.form['BusinessId']

    response = Form1099NEC.getForm1099NECList(selectedBusiness)

    recipientNameList = []

    if response is not None:

        if 'Form1099Records' in response:

            if response['Form1099Records'] is not None:

                for records in response['Form1099Records']:
                    recipientData = RecipientModel()
                    recipientData.set_RecipientId(records['Recipient']['RecipientId'])
                    recipientData.set_FirstPayeeNm(records['Recipient']['RecipientNm'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientNameList.append(recipientData.__dict__)

    return json.dumps(recipientNameList)


@appInstance.route('/FormNecList', methods=['GET'])
def get_nec_list():

    get_business_request = BusinessListRequest()

    get_business_request.set_page(1)

    get_business_request.set_page_size(50)

    get_business_request.set_from_date('03/20/2021')

    get_business_request.set_to_date('04/31/2021')

    response = Business.get_business_list(get_business_request)

    businesses = response['Businesses']

    print(businesses)

    return render_template('form_1099_nec_list.html', businesses=businesses)


@appInstance.route('/nec_list', methods=['POST'])
def form1099NecList():

    get_nec_request = GetNecListRequest()

    get_nec_request.set_business_id(request.form['BusinessId'])

    get_nec_request.set_page(1)

    get_nec_request.set_page_size(50)

    get_nec_request.set_from_date('03/20/2021')

    get_nec_request.set_to_date('04/31/2021')

    response = Business.get_nec_list(get_nec_request)

    print(response)

    form1099NecList = []

    if response is not None:

        if 'Form1099Records' in response:

            if response['Form1099Records'] is not None:

                for records in response['Form1099Records']:
                    recipientData = Form1099NecList()
                    recipientData.set_RecipientNm(records['Recipient']['RecipientNm'])
                    recipientData.set_TIN(records['Recipient']['TIN'])
                    recipientData.set_RecipientId(records['Recipient']['RecordId'])
                    recipientData.set_SubmissionId(records['SubmissionId'])
                    recipientData.set_BusinessNm(records['BusinessNm'])
                    form1099NecList.append(recipientData.__dict__)

    return json.dumps(form1099NecList)


# Entry point for application
if __name__ == '__main__':
    appInstance.debug = True
    appInstance.run()
