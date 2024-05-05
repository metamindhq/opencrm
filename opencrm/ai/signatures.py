import dspy


class AntecedentSignature(dspy.Signature):
    patient_conversation = dspy.InputField(desc="Problem patient is facing right now stated by patient themself")
    past_diagnosis = dspy.InputField(desc="Comma separated past diagnosis of the patient")
    past_habits = dspy.InputField(desc="comma separated bad habits of the patients")
    antecedents = dspy.OutputField(desc="JSON list of string of the antecedents of the possible diseases faced by the "
                                        "current patient IMPORTANT!! This must be a JSON list of string")


class SymptomsSignature(dspy.Signature):
    patient_conversation = dspy.InputField(desc="Problem patient is facing right now stated by patient themself")
    symptoms = dspy.OutputField(desc="JSON list of string of possible symptoms we can detect from the patient's "
                                     "conversation, IMPORTANT!! This must be a JSON list of string")


class DiagnosisSignature(dspy.Signature):
    antecedents = dspy.InputField(desc="The antecedents of the patient")
    symptoms = dspy.InputField(desc="The symptoms of the patient")
    bmi = dspy.InputField(desc="BMI of the patient")
    possible_diseases = dspy.OutputField(
        desc="JSON list of string of two possible diagnosed disease, e.g ['anemia','tuberculosis'], IMPORTANT!! This "
             "must"
             "follow a comma separated list of values")


class SelectSpecializationSignature(dspy.Signature):
    specializations = dspy.InputField(desc="Comma separated specialized doctors available in hospital")
    diagnosed_diseases = dspy.InputField(desc="Comma separated predicted possible diseases")
    selected_specialization = dspy.OutputField(desc="Single word output of suitable specialization patient should "
                                                    "visit for the possible diagnosed disease")


class PatientInteractionSignature(dspy.Signature):
    patient_conversation = dspy.InputField(desc="Problem patient is facing right now stated by patient themself")
    past_diagnosis = dspy.InputField(desc="Comma separated past diagnosis of the patient")
    past_habits = dspy.InputField(desc="comma separated bad habits of the patients")
