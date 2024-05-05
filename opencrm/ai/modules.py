import dspy
import json

from opencrm.ai.signatures import AntecedentSignature, SymptomsSignature, DiagnosisSignature, \
    SelectSpecializationSignature, DrugDrugInteractionSignature


def is_comma_separated_list(string):
    # Validate if the output is a comma-separated JSON list
    string = string.strip()
    val = json.loads(string)
    if not isinstance(val, list):
        return False
    else:
        return True


failed_assertion_message = """Output must be a comma-separated list!
Please ensure the output is a JSON list separated by commas
"""


def is_single_word(string):
    string = string.strip()
    if " " in string:
        return False
    else:
        return True


single_word_assertion_message = """
Output must be a single word!
Please remove any spaces or special characters from the output
"""


class Antecedent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(AntecedentSignature)

    def forward(self, conversation, past_diagnosis, past_habits):
        output = self.gen(patient_conversation=conversation,
                          past_diagnosis=past_diagnosis,
                          past_habits=past_habits)
        dspy.Suggest(is_comma_separated_list(output.antecedents), failed_assertion_message)
        return output.antecedents


class Symptoms(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(SymptomsSignature)

    def forward(self, conversation):
        output = self.gen(patient_conversation=conversation).symptoms
        dspy.Suggest(is_comma_separated_list(output), failed_assertion_message)
        return output


class Diagnosis(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(DiagnosisSignature)

    def forward(self, antecedents, symptoms, bmi):
        output = self.gen(antecedents=antecedents,
                          symptoms=symptoms,
                          bmi=bmi).possible_diseases
        dspy.Suggest(is_comma_separated_list(output), failed_assertion_message)
        return output


class SelectSpecialization(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(SelectSpecializationSignature)

    def forward(self, specializations, diagnosed_diseases):
        output = self.gen(specializations=specializations,
                          diagnosed_diseases=diagnosed_diseases).selected_specialization
        return output


def patient_details(conversation, past_diagnosis, past_habits, bmi):
    antecedents = Antecedent().forward(conversation, past_diagnosis, past_habits)
    symptoms = Symptoms().forward(conversation)
    diagnosis = Diagnosis().forward(antecedents, symptoms, bmi)
    summary = {
        'antecedents': antecedents,
        'symptoms': symptoms,
        'diagnosis': diagnosis
    }
    return summary


class DrugDrugInteraction(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(DrugDrugInteractionSignature)

    def forward(self, drugs, prescribed_drugs):
        gen = self.gen(drugs=drugs,
                       prescribed_drugs=prescribed_drugs)
        is_interactive = gen.interactions
        interaction_details = gen.interaction_details
        return {
            'is_interactive': is_interactive,
            'interaction_details': interaction_details
        }
