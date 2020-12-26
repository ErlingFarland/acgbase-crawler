from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, List

from lib.data.result.utils import empty_dict, empty_class, empty_list, RGender, RValue


@dataclass
class AgeRange:
    min: int
    max: int


@dataclass
class RChar_CV:
    name: Optional[str] = None
    language: List[str] = empty_list()
    tags: List[str] = empty_list()


@dataclass
class RChar_ComponentOutlook:
    color: Optional[str] = None
    shape: List[str] = empty_list()
    features: List[str] = empty_list()

@dataclass
class RChar_ValueDesc:
    value: Optional[RValue] = None
    tags: List[str] = empty_list()


@dataclass
class RChar_BodyOutlook:
    eyes: RChar_ComponentOutlook = empty_class(RChar_ComponentOutlook)
    eyebrows: RChar_ComponentOutlook = empty_class(RChar_ComponentOutlook)
    hair: RChar_ComponentOutlook = empty_class(RChar_ComponentOutlook)
    height: RChar_ValueDesc = empty_class(RChar_ValueDesc)
    weight: RChar_ValueDesc = empty_class(RChar_ValueDesc)
    gender: Optional[RGender] = None
    age: RChar_ValueDesc = empty_class(RChar_ValueDesc)
    age_range: Optional[AgeRange] = None
    fur: List[str] = empty_list()
    skin_color: List[str] = empty_list()
    race: List[str] = empty_list()
    ears: List[str] = empty_list()
    face_shape: List[str] = empty_list()
    disease: List[str] = empty_list()
    hand_features: List[str] = empty_list()
    mouth: List[str] = empty_list()
    tags: List[str] = empty_list()

@dataclass
class RChar_ClothOutlook:
    gender: Optional[RGender] = None
    features: List[str] = empty_list()

@dataclass
class RChar_Outlook:
    body: RChar_BodyOutlook = empty_class(RChar_BodyOutlook)
    clothing: RChar_ClothOutlook = empty_class(RChar_ClothOutlook)


@dataclass
class RChar_VoiceTimbre:
    gender: Optional[RGender] = None
    age_range: Optional[AgeRange] = None
    features: List[str] = empty_list()


class RChar_VoicePitch(Enum):
    ultra_low = 'ultra_low'
    low = 'low'
    average = 'average'
    high = 'high'
    ultra_high = 'ultra_high'


@dataclass
class RChar_Voice:
    cv: List[RChar_CV] = empty_list()
    timbre: RChar_VoiceTimbre = empty_class(RChar_VoiceTimbre)
    pitch: Optional[RChar_VoicePitch] = None

@dataclass
class RChar_Personality:
    age: RChar_ValueDesc = empty_class(RChar_ValueDesc)
    age_range: AgeRange = empty_class(AgeRange)
    features: List[str] = empty_list()
    habits: List[str] = empty_list()
    weapons: List[str] = empty_list()

@dataclass
class RChar_CharName:
    name: str
    language: Optional[str] = None
    tags: List[str] = empty_list()

@dataclass
class RChar_SocialRelationship:
    family: List[str] = empty_list()
    job: List[str] = empty_list()
    ethnic_group: List[str] = empty_list()
    love: List[str] = empty_list()
    friend: List[str] = empty_list()
    identity: List[str] = empty_list()
    luck: List[str] = empty_list()


@dataclass
class RCharacter:
    page_name: str
    belongs_to: List[str] = empty_list()
    age: RChar_ValueDesc = empty_class(RChar_ValueDesc)
    names: List[RChar_CharName] = empty_list()
    outlook: RChar_Outlook = empty_class(RChar_Outlook)
    personality: RChar_Personality = empty_class(RChar_Personality)
    social_relationship: RChar_SocialRelationship = empty_class(RChar_SocialRelationship)
    tags: List[str] = empty_list()
