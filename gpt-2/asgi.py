import uvicorn
from rest import app

uvicorn.run(app, 
    host='0.0.0.0', 
    port=8000, 
    reload=False)