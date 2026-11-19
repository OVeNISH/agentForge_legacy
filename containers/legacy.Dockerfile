FROM python:2.7.18-slim
COPY containers/smoke.py /opt/modernize/smoke.py
USER 65534:65534
ENTRYPOINT ["python", "-B", "/opt/modernize/smoke.py"]
