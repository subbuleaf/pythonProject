import requests
import json
from utils import HeaderUtils, Config, EndPointConfig
from api_services import JwtGeneration
from core.CreateForm1099NECModel import CreateForm1099NECModel
from core.SubmissionManifestModel import SubmissionManifestModel
from core.StatesModel import StatesModel
from core.ReturnHeaderModel import ReturnHeaderModel
from core.ReturnDataModel import ReturnDataModel
from core.NECFormDataModel import NECFormDataModel
from core.RecipientModel import RecipientModel
from core.CreateBusinessRequest import CreateBusinessRequest
from core.ForeignAddress import ForeignAddress


def create(businessId, recipientId, rName, rTIN, amount):
    requestModel = CreateForm1099NECModel()

    returnHeader = ReturnHeaderModel()
    businessModel = CreateBusinessRequest()
    # businessModel.set_BusinessId("0fd6e0a3-f122-4cdc-a4da-25cb155010e1")
    businessModel.set_BusinessId(businessId)
    returnHeader.set_Business(businessModel.__dict__)
    requestModel.set_ReturnHeader(returnHeader.__dict__)

    submissionManifest = SubmissionManifestModel()
    # submissionManifest.set_SubmissionId(null)
    submissionManifest.set_TaxYear(2020)
    submissionManifest.set_IsFederalFiling(2020)
    submissionManifest.set_IsStateFiling(True)
    submissionManifest.set_IsPostal(True)
    submissionManifest.set_IsOnlineAccess(True)
    submissionManifest.set_IsTinMatching(True)
    submissionManifest.set_IsScheduleFiling(True)
    scheduleFiling = SubmissionManifestModel()
    scheduleFiling.set_EfileDate("04/05/2021")
    submissionManifest.set_ScheduleFiling(scheduleFiling.__dict__)
    requestModel.set_SubmissionManifest(submissionManifest.__dict__)
    returnDataList = []
    returnData = ReturnDataModel()
    # returnData.set_RecordId(null)
    returnData.set_SequenceId("1")
    # set Recipient data
    recipientModel = RecipientModel()
    if recipientId != '-1':
        recipientModel.set_RecipientId(recipientId)

    recipientModel.set_TINType("EIN")
    recipientModel.set_TIN(rTIN)
    recipientModel.set_FirstPayeeNm(rName)
    recipientModel.set_SecondPayeeNm("")
    recipientModel.set_IsForeign(False)
    usAddress = ForeignAddress()
    usAddress.set_Address1("1751 Kinsey Rd")
    usAddress.set_Address2("Main St")
    usAddress.set_City("Dothan")
    usAddress.set_State("AL")
    usAddress.set_ZipCd("36303")
    recipientModel.set_USAddress(usAddress.__dict__)
    # recipientModel.set_ForeignAddress(null)
    recipientModel.set_Email("sharmila.k@dotnetethics.com")
    recipientModel.set_Fax("1234567890")
    recipientModel.set_Phone("1234567890")
    returnData.set_Recipient(recipientModel.__dict__)
    # set NEC data
    necFormDataModel = NECFormDataModel()
    necFormDataModel.set_B1NEC(amount)
    necFormDataModel.set_B4FedTaxWH(54.12)
    necFormDataModel.set_IsFATCA(True)
    necFormDataModel.set_Is2ndTINnot(True)
    necFormDataModel.set_AccountNum("20123130000009000001")
    statesList = []
    stateModel = StatesModel()
    stateModel.set_StateCd("PA")
    stateModel.set_StateWH(15)
    stateModel.set_StateIdNum("99999999")
    stateModel.set_StateIncome(16)
    statesList.append(stateModel.__dict__)  # State 1
    stateModel = StatesModel()
    stateModel.set_StateCd("AZ")
    stateModel.set_StateWH(17)
    stateModel.set_StateIdNum("99-999999")
    stateModel.set_StateIncome(18)
    statesList.append(stateModel.__dict__)  # State 2
    necFormDataModel.set_States(statesList)

    returnData.set_NECFormData(necFormDataModel.__dict__)
    returnDataList.append(returnData.__dict__)

    requestModel.set_ReturnData(returnDataList)

    print(f"Create Form 1099 NEC request{requestModel.__dict__}")

    response = requests.post(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.CREATE_FORM1099_NEC,
                             data=json.dumps(requestModel.__dict__),
                             headers=HeaderUtils.getheaders())

    if response.status_code == 200:

        return response


def getForm1099NECList(businessId):
    print(Config.apiBaseUrls[
              'TBS_API_BASE_URL'] + EndPointConfig.GET_FORM1099_NEC_LIST + " PARAMS = BusinessId:" + businessId)

    response = requests.get(Config.apiBaseUrls['TBS_API_BASE_URL'] + EndPointConfig.GET_FORM1099_NEC_LIST,
                            params={"BusinessId": businessId}, headers=HeaderUtils.getheaders())

    print(response.json())

    return response.json()
