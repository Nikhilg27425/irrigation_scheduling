"""
Simple translation helper using Google Translate API
"""
from googletrans import Translator

translator = Translator()

# Language codes for 22 Indian languages
INDIAN_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'ur': 'Urdu',
    'sa': 'Sanskrit',
    'ks': 'Kashmiri',
    'sd': 'Sindhi',
    'ne': 'Nepali',
    'kok': 'Konkani',
    'mni': 'Manipuri',
    'doi': 'Dogri',
    'sat': 'Santali',
    'mai': 'Maithili'
}

def translate_text(text, target_lang='en'):
    """Translate text to target language"""
    try:
        if target_lang == 'en':
            return text
        
        # Map some languages that googletrans might not support directly
        lang_map = {
            'kok': 'mr',  # Konkani -> Marathi (similar)
            'mni': 'bn',  # Manipuri -> Bengali (similar script)
            'doi': 'hi',  # Dogri -> Hindi (similar)
            'sat': 'hi',  # Santali -> Hindi
            'mai': 'hi'   # Maithili -> Hindi (similar)
        }
        
        translate_lang = lang_map.get(target_lang, target_lang)
        result = translator.translate(text, dest=translate_lang)
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def get_translations(lang_code='en'):
    """Get common UI translations for a language"""
    translations = {
        'dashboard': 'Dashboard',
        'weather': 'Weather',
        'irrigation': 'Irrigation Model',
        'api_management': 'API Management',
        'profile': 'Profile',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'farm_name': 'Farm Name',
        'location': 'Location',
        'farm_size': 'Farm Size',
        'welcome': 'Welcome',
        'irrigation_needed': 'Irrigation Needed',
        'no_irrigation': 'No Irrigation Needed',
        'predict': 'Predict',
        'crop_type': 'Crop Type',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'soil_moisture': 'Soil Moisture',
        'crop_days': 'Crop Days'
    }
    
    if lang_code == 'en':
        return translations
    
    # Translate all keys
    translated = {}
    for key, value in translations.items():
        translated[key] = translate_text(value, lang_code)
    
    return translated
