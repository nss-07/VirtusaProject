from flask import Flask, jsonify, render_template, request
import pymongo
import random
import AI_ML

app = Flask(__name__)
MONGO_URI = "mongodb+srv://aladsss:lpacafcs@unogame.oxplv.mongodb.net/Virtusa?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&connect=false"

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def test():
    return render_template("index.html")

@app.route('/signin', methods=['POST'])
def signin():
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]
    users = db["userdata"]


    data = request.form
    print(type(data))


    user = users.find_one({ "Mail": data["email"], "Password": data["password"] })
    print(user)
    print(type(user))
    if user:

        if (data["email"] == 'ADM@mail.com'):
            pending = db["pending"]
            pendrecs = []
            for record in pending.find():
                # print(record)
                record["age"] = random.randint(10,100)
                record["hospitalization_time"] = str(random.randint(1,31))+"/"+str(random.randint(1,12))+"/"+str(random.randint(1950,2020))
                record["discharge_time"] = str(int(record["hospitalization_time"][:1])+1) + record["hospitalization_time"][2:]

                pendrecs.append(record)

            print(pendrecs)
            return render_template("admin_portal.html", data={"pending": pendrecs})

        # print(current.count_documents({"refif": user["refid"]}))

        current = db["Current"]
        currecs = []
        for record in current.find({"hospital_id": user["Hospital_id"]}):
            # print(record)
            # d = dict(record)
            # print(d)
            currecs.append(record)



        pending = db["pending"]
        pendrecs = []
        for record in pending.find({"hospital_id": user["Hospital_id"]}):
        #     # print(record)
            pendrecs.append(record)

        review = db["review"]
        revrecs = []
        for record in review.find({"hospital_id": user["Hospital_id"]}):
            revrecs.append(record)

        print("Currents:\n",currecs)
        print("Pending:\n",pendrecs)
        print("Reviewed:\n",revrecs)
        # return users.find_one()
        return render_template("dashboard.html",data={"current": currecs, "pending": pendrecs, "review": revrecs, "hospital_id": user["Hospital_id"]})
        # return render_template("testing.html", data={"current": currecs})
        # return "Done!"
        client.close()
    else:
        return "KUCH NAHI CHALA!!!"

@app.route('/get-details', methods=["POST"])
def get_details():
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]

    claimsdata = db["claimsdata"]

    data = request.form

    print(data)
    claim = claimsdata.find_one({"policy_number": data["id"]})
    print("YO")

    if(claim):

        if(claim["fraud_reported"] == "Y"):
            claim_playment=0
        elif(claim["claim_status_category_code"] == 'F1'):
            claim_payment = float(claim["total_claim_amount"]) * 0.9
        else:
            claim_payment = float(claim["total_claim_amount"]) * 0.75
        client.close()
        return render_template("print_details.html", data={
            "insured": claim["p_fname"] + " " + claim["p_lname"],
            "dob": data["dob"],
            "gender": data["gender"],
            "memberid": claim["policy_number"],
            "service_provider": claim["service_provider"],
            "status": claim["claim_status_category_code"],
            "status_date": claim["hospitalized_date"],
            "claim_amount": claim["total_claim_amount"],
            "claim_payment": claim_playment
        })


@app.route('/inpatient')
def inpatient():
    data = dict(request.args)
    print(data)
    return render_template("inpatient.html", data=data)

@app.route('/submit-inpatient', methods=["POST"])
def submit_inpatient():
    data = dict(request.form)
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]

    current = db["Current"]
    current.insert_one(data)
    print("YO")

    currecs = []
    for record in current.find({"hospital_id": data["hospital_id"]}):
        currecs.append(record)

    pending = db["pending"]
    pendrecs = []
    for record in pending.find({"hospital_id": data["hospital_id"]}):
        # print(record)
        pendrecs.append(record)

    review = db["review"]
    revrecs = []
    for record in review.find({"hospital_id": data["hospital_id"]}):
        revrecs.append(record)

    print("Currents:\n", currecs)
    print("Pending:\n", pendrecs)
    print("Reviewed:\n", revrecs)
    # return users.find_one()

    client.close()
    return render_template("dashboard.html", data={"current": currecs, "pending": pendrecs, "review": revrecs,
                                                   "hospital_id": data["hospital_id"]})

    # return render_template('dashboard.html',)

@app.route('/outpatient')
def outpatient():
    data = request.args
    print(data)


    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]

    current = db["Current"]
    claim = current.find_one({"policy_number": data["policy_number"], "hospital_id": data["hospital_id"]})

    if(claim):
        client.close()
        return render_template("outpatient.html", data=claim)
    else:
        currecs = []
        for record in current.find({"hospital_id": data["hospital_id"]}):
            currecs.append(record)

        pending = db["pending"]
        pendrecs = []
        for record in pending.find({"hospital_id": data["hospital_id"]}):
            # print(record)
            pendrecs.append(record)

        review = db["review"]
        revrecs = []
        for record in review.find({"hospital_id": data["hospital_id"]}):
            revrecs.append(record)

        print("Currents:\n", currecs)
        print("Pending:\n", pendrecs)
        print("Reviewed:\n", revrecs)
        # return users.find_one()

        client.close()
        return render_template("dashboard.html", data={"current": currecs, "pending": pendrecs, "review": revrecs,
                                                       "hospital_id": data["hospital_id"]})

@app.route('/submit-outpatient', methods=["POST"])
def submit_outpatient():

    data = request.form
    print(data)

    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]

    current = db["Current"]
    claim = current.find_one({"hospital_id": data["hospital_id"], "policy_number": data["policy_number"]})
    if(claim):
        current.delete_one({"policy_number": data["policy_number"]})
        for key,val in data.items():
            claim[key] = data[key]


        del claim["_id"]

        claim["claim_status_category_code"] = "PROCESSING"

        flag=AI_ML.callAI(claim)
        print(flag)

        if flag==1 :
            review = db["review"]
            review.insert_one(claim)
            currecs = []
            for record in current.find({"hospital_id": data["hospital_id"]}):
                currecs.append(record)

            pending = db["pending"]
            pendrecs = []
            for record in pending.find({"hospital_id": data["hospital_id"]}):
                # print(record)
                pendrecs.append(record)

            review = db["review"]
            revrecs = []
            for record in review.find({"hospital_id": data["hospital_id"]}):
                revrecs.append(record)

            print("Currents:\n", currecs)
            print("Pending:\n", pendrecs)
            print("Reviewed:\n", revrecs)
            client.close()
            return render_template("dashboard.html", data={"current": currecs, "pending": pendrecs, "review": revrecs,
                                                       "hospital_id": data["hospital_id"]})
        else:
            pending = db["pending"]
            pending.insert_one(claim)
            print(claim)

            currecs = []
            for record in current.find({"hospital_id": data["hospital_id"]}):
                currecs.append(record)

            pending = db["pending"]
            pendrecs = []
            for record in pending.find({"hospital_id": data["hospital_id"]}):
                # print(record)
                pendrecs.append(record)

            review = db["review"]
            revrecs = []
            for record in review.find({"hospital_id": data["hospital_id"]}):
                revrecs.append(record)

            print("Currents:\n", currecs)
            print("Pending:\n", pendrecs)
            print("Reviewed:\n", revrecs)
            client.close()
            return render_template("dashboard.html", data={"current": currecs, "pending": pendrecs, "review": revrecs,
                                                       "hospital_id": data["hospital_id"]})

@app.route('/pass-patient')
def pass_patient():

    data = request.args
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]
    pending = db["pending"]
    claim = pending.find_one({"policy_number": data["policy_number"]})
    if(claim):
        pending.delete_one(claim)
        claim["claim_status_category_code"]="PASS"
        review = db["review"]
        review.insert_one(claim)

    pending = db["pending"]
    pendrecs = []

    for record in pending.find():
        pendrecs.append(record)

    return render_template("admin_portal.html",data={"pending": pendrecs})


@app.route('/fail-patient')
def fail_patient():
    data = request.args
    client = pymongo.MongoClient(MONGO_URI)
    db = client["Virtusa"]
    pending = db["pending"]
    claim = pending.find_one({"policy_number": data["policy_number"]})
    if (claim):
        pending.delete_one(claim)
        claim["claim_status_category_code"] = "FAIL"
        review = db["review"]
        review.insert_one(claim)

    pending = db["pending"]
    pendrecs = []

    for record in pending.find():
        pendrecs.append(record)

    return render_template("admin_portal.html", data={"pending": pendrecs})




if __name__ == '__main__':
    app.run()
