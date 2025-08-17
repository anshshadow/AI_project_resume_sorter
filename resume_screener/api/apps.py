from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model. This will be downloaded on first run.
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
    return text

def extract_text_from_file(file):
    """Detects file type and extracts text accordingly."""
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        # Basic text extraction for other file types, might not be accurate
        try:
            return file.read().decode('utf-8')
        except:
            return ""

def calculate_similarity(jd_text, resume_text):
    """
    Calculates the cosine similarity between job description and resume text.
    Returns a score between 0 and 100.
    """
    if not jd_text or not resume_text:
        return 0

    # Generate embeddings for both texts
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Compute cosine-similarity
    cosine_scores = util.pytorch_cos_sim(jd_embedding, resume_embedding)
    
    # The result is a tensor, get the float value and scale to 0-100
    score = cosine_scores.item() * 100
    
    # Ensure score is within a realistic range (e.g., not negative)
    return max(0, min(100, score))

