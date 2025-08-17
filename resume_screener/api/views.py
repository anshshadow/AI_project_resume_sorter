from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import JobDescription, Resume
from .serializers import UserSerializer, JobDescriptionSerializer, ResumeSerializer
from .ai_logic import extract_text_from_file, calculate_similarity

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class JobDescriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(hr=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(hr=self.request.user)

class JobDescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(hr=self.request.user)

class ResumeListView(generics.ListAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return Resume.objects.filter(job_description__id=job_id, job_description__hr=self.request.user)

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(job_description__hr=self.request.user)

class ResumeUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id, *args, **kwargs):
        try:
            job_description = JobDescription.objects.get(id=job_id, hr=request.user)
        except JobDescription.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist('resumes')
        if not files:
            return Response({"error": "No resume files provided."}, status=status.HTTP_400_BAD_REQUEST)
            
        created_resumes = []
        
        # Combine job title, description, and skills for a comprehensive job profile text
        jd_text = f"{job_description.title} {job_description.description} {job_description.skills}"

        for file in files:
            # Extract text from the uploaded resume file
            resume_text = extract_text_from_file(file)

            if not resume_text:
                # If text extraction fails, we can't score it.
                # We can either skip it or save with a score of 0.
                # Here, we'll save it with a score of 0 and a remark.
                score = 0
                remarks = "Could not parse resume file."
            else:
                # Calculate the similarity score using our AI logic
                score = calculate_similarity(jd_text, resume_text)
                remarks = ""

            resume = Resume.objects.create(
                job_description=job_description,
                file=file,
                name=file.name,
                score=round(score, 2),
                remarks=remarks
            )
            created_resumes.append(ResumeSerializer(resume).data)

        return Response(created_resumes, status=status.HTTP_201_CREATED)
