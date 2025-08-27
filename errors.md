1.) requirement.txt → should be requirements.txt
2.) Removed onnxruntime==1.18.0 from requirements.txt- No need to mention onnxruntime explicitly, since it will be installed as a dependency when you will install crew ai.
3.) Replaced opentelemetry-api==1.25.0 in requirements.txt with opentelemetry-api==1.30.0 as crewai 0.130.0 enforces >=1.30.0 for opentelemetry-api.
4.) All OpenTelemetry components must be on the same version family so 1.25.0 → 1.30.0.
5.) crewai==0.130.0 explicitly requires:pydantic>=2.4.2 but it is pydantic==1.10.13 so fixed this with latest version pydantic==2.7.4.
6.) Remove pydantic_core entirely (pip will install the correct matching version automatically).
7.) Upgrade Click to at least 8.1.8 as crewai==0.130.0 accepts any Click >=8.1.7.
8.) Upgrade from google-api-core==2.10.0 to google-api-core==2.19.1 as google-ai-generativelanguage==0.6.4 does not supports it. 
9.) opentelemetry-semantic-conventions==0.51b0 is compatible in place of opentelemetry-semantic-conventions==0.47b0 which was mentioned earlier.
10.) Upgrade to protobuf==5.27.2
11.) openai>=1.68.2
12.) Unpin langsmith==0.1.67 → replace with langsmith>=0.3.18,<0.4.0
13.) Explicitly add tiktoken>=0.8.0
14-) Explicitly add chromadb>=0.5.23