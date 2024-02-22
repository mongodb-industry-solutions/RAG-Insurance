import itertools
import random
from datetime import datetime, timedelta
from pymongo import MongoClient

claimDescriptionList = [
    "During a heavy thunderstorm, a vehicle lost traction and slid into a guardrail on the highway, causing a multi-car pileup.",
    "A distracted driver failed to notice stopped traffic ahead, resulting in a high-speed rear-end collision.",
    "A vehicle attempted to avoid a suddenly crossing deer, veering off the road and colliding with a tree.",
    "Two vehicles collided at an intersection after one ran a red light, causing a T-bone crash.",
    "A car parked on a steep hill rolled down after the handbrake failed, hitting another parked vehicle.",
    "High winds caused a tree branch to fall directly onto a moving car, damaging the roof and windshield.",
    "A vehicle's tire blew out on the freeway, causing the driver to lose control and crash into the median.",
    "During a blizzard, a car skidded on ice and rear-ended a snow plow stopped at a red light.",
    "A vehicle swerved to miss an obstacle on the road, hitting a pedestrian barrier and flipping over.",
    "In a busy parking lot, a car reversed without noticing an approaching vehicle, causing a collision.",
    "A sudden hailstorm damaged vehicles on the road, breaking windshields and causing multiple accidents.",
    "A car attempting to change lanes without signaling clipped another car, spinning it out of control.",
    "At night, a vehicle hit a pothole at high speed, damaging its front axle and causing it to veer off the road.",
    "A motorist driving the wrong way on a one-way street collided head-on with an oncoming vehicle.",
    "During a street race, one of the cars lost control, crashing into a barrier and then a lamp post.",
    "A vehicle's brakes failed at a traffic light, causing it to crash into the car in front of it.",
    "A large truck overturned while taking a sharp turn too quickly, blocking the road and causing a multi-vehicle collision.",
    "A car was side-swiped by another vehicle attempting to merge into its lane on a busy highway.",
    "In dense fog, a vehicle did not see a stopped truck ahead, crashing into its rear at moderate speed.",
    "A vehicle parked illegally was struck by a bus trying to navigate through a narrow street."
]

damageDescriptionList = [
    "Guardrail impact caused significant front-end damage, leading to a chain reaction of collisions with multiple vehicles involved.",
    "Rear bumper crushed, trunk caved in, and rear windshield shattered from the high-speed impact.",
    "Significant side and front-end damage from hitting the tree, with the vehicle's airbags deployed.",
    "Severe damage to the vehicle's side, with the door and adjacent panels crumpled and windows broken.",
    "Rear-end damage to the rolling car and front-end damage to the struck vehicle, with minor scratches and dents.",
    "Roof caved in and front windshield cracked from the impact of the falling tree branch.",
    "Front-end damage from median collision, with tire and wheel assembly completely destroyed.",
    "Rear-end damage including bumper and taillight destruction, with minor damage to the snow plow.",
    "Side damage from hitting the barrier and roof damage from the vehicle flipping over.",
    "Rear bumper and tailgate of the reversing car damaged, with the front bumper of the other vehicle also impacted.",
    "Multiple dents and shattered windshields from hailstones, with some vehicles having hood damage.",
    "Side panel and rear bumper damage, with the spun vehicle also having front-end damage.",
    "Front axle broken, bumper and hood damage from the pothole impact, and subsequent collision with roadside objects.",
    "Front-ends of both vehicles heavily damaged, with radiators, headlights, and bumpers destroyed.",
    "Front-end crushed against the barrier, side and rear damage from colliding with the lamp post.",
    "Front bumper and hood crumpled, with damage to the radiator and engine compartment.",
    "Truck sustained side and top damage from overturning, with debris causing additional damage to nearby vehicles.",
    "Side panel scraped and mirror knocked off, with minor damage to the merging vehicle.",
    "Rear-end of the truck undamaged, but the colliding vehicle's front end is significantly damaged.",
    "Side panel and wheel of the illegally parked car damaged, with minor damage to the bus."
]


# MongoDB Atlas connection string
mongo_conn_str = "mongodb+srv://luca:abba@ist-shared.n0kts.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_conn_str)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client.demo_rag_insurance
collection = db.claims_final

def generate_document(customer_id, policy_number, claim_id, claim_status_code, 
                      claim_description, damage_description, coverages_list):
    document = {
        "customerID": customer_id,
        "policyNumber": policy_number,
        "claimID": claim_id,
        "claimStatusCode": claim_status_code,
        "claimDescription": claim_description,
        "totalLossAmount": random.randint(1, 5000),
        "claimFNOLDate": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
        "claimClosedDate": (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
        "claimLineCode": "Auto",
        "damageDescription": damage_description,
        "insurableObject": {
            "insurableObjectId": "abc" + customer_id[1:],
            "vehicleMake": "Make" + customer_id[1:],
            "vehicleModel": "Model" + claim_id[2:]
        },
        "coverages": [{"coverageCode": "888", "description": "3rd party responsible"}] + 
                     [random.choice(coverages_list)]
    }
    return document

claim_status_codes = ["Active", "Closed", "Subrogation"]
additional_coverage_options = [
    {"coverageCode": "999", "description": "accidental driver-responsible damage"},
    {"coverageCode": "777", "description": "Vehicle rental/loaner service for customer"},
    {"coverageCode": "666", "description": "Glass windshield repair"},
    {"coverageCode": "555", "description": "Autobody and paint repair"}
]

# Create iterators for claim descriptions, damage descriptions, and claim status codes
claim_description_iter = itertools.cycle(claimDescriptionList)
damage_description_iter = itertools.cycle(damageDescriptionList)
claim_status_code_iter = itertools.cycle(claim_status_codes)

documents = []
for i in range(20):
    documents.append(generate_document(f"c{i+100}", f"p{i+100}", f"cl{i+100}", 
                                        next(claim_status_code_iter), 
                                        next(claim_description_iter), 
                                        next(damage_description_iter), 
                                        additional_coverage_options))

collection.insert_many(documents)
print("Documents successfully written to MongoDB Atlas.")