import requests
from core.ForeignAddress import ForeignAddress
from core.GetBusinssList import BusinessListRequest
import json
from utils import HeaderUtils, Config, EndPointConfig
from core.CreateBusinessRequest import CreateBusinessRequest
from core.SigningAuthority import SigningAuthority
from api_services import JwtGeneration

# Create the new Business
def create(businessName, einOrSSN):

    requestModel = CreateBusinessRequest()
    requestModel.set_BusinessNm(businessName)
    # requestModel.set_IsEIN(request.form['is_ein'])
    requestModel.set_EINorSSN(einOrSSN)
    # requestModel.set_TradeNm(request.form['trade_nm'])
    # requestModel.set_Email(request.form['email'])
    # requestModel.set_ContactNm(request.form['contact_nm'])
    # requestModel.set_Phone(request.form['phone'])
    # requestModel.set_PhoneExtn(request.form['phone_extn'])
    # requestModel.set_Fax(request.form['fax'])
    # requestModel.set_BusinessType(request.form['business_Type'])
    # requestModel.set_KindOfEmployer(request.form['kind_of_employer'])
    # requestModel.set_KindOfPayer(request.form['kind_of_payer'])
    # requestModel.set_IsBusinessTerminated(request.form['is_business_terminated'])
    # requestModel.set_IsForeign(request.form['is_foreign'])
    requestModel.set_IsEIN(True)
    requestModel.set_TradeNm("kodak")
    requestModel.set_Email("sharmila.k+123@dotnetethics.com")
    requestModel.set_ContactNm("John")
    requestModel.set_Phone("1234567890")
    requestModel.set_PhoneExtn("12345")
    requestModel.set_Fax("1234567890")
    requestModel.set_BusinessType("ESTE")
    requestModel.set_KindOfEmployer("FEDERALGOVT")
    requestModel.set_KindOfPayer("REGULAR941")
    requestModel.set_IsBusinessTerminated(False)
    requestModel.set_IsForeign(True)

    saModel = SigningAuthority()
    # saModel.set_SAName(request.form['sa_name'])
    # saModel.set_SAPhone(request.form['sa_phone'])
    # saModel.set_SABusinessMemberType(request.form['business_member_type'])
    saModel.set_SAName("John")
    saModel.set_SAPhone("1234567890")
    saModel.set_SABusinessMemberType("ADMINISTRATOR")

    requestModel.set_SigningAuthority(saModel.__dict__)

    addressModel = ForeignAddress()
    addressModel.set_Address1("22 St")
    addressModel.set_Address2("Clair Ave E")
    addressModel.set_City("Toronto")
    addressModel.set_ProvinceOrStateNm("Ontario")
    addressModel.set_Country("CK")
    addressModel.set_PostalCd("M1R 0E9")

    requestModel.set_ForeignAddress(addressModel.__dict__)

    jwtToken = JwtGeneration.get_jwt_token()

    print(jwtToken)

    access_token = JwtGeneration.get_access_token_by_jwt_token(jwtToken)

    # inputData = json.dumps(CreateBusinessRequest.create(requestModel))

    convertedModel = json.dumps(requestModel.__dict__)

    print(f"Request Model = {convertedModel}")
    # print(json.dumps(requestModel))
    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_BUSINESS,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    print(f'statuscode = {response.status_code}')
    print(f'response header = {response.text}')

    json_obj = json.loads(response.text)
    return json_obj


# Get Business Information by using BusinessId and EIN
def get_business_detail(BusinessId, EIN):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS,
                            params={"BusinessId": BusinessId, "EIN": EIN}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()


# Get Business List
def get_business_list(get_business_request: BusinessListRequest):
    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_BUSINESS_LIST,
                            params={"Page": get_business_request.get_page(),
                                    "PageSize": get_business_request.get_page_size(),
                                    "FromDate": get_business_request.get_from_date(),
                                    "ToDate": get_business_request.get_to_date()}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()
