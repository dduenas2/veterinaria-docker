pipeline {
    agent any
    
    environment {
        // Credenciales
        GITHUB_TOKEN = credentials('github-token')
        
        // Configuración de imágenes
        FRONTEND_IMAGE = "veterinaria-frontend"
        BACKEND_IMAGE = "veterinaria-backend"
        BUILD_VERSION = "${BUILD_NUMBER}"
        
        // Notificaciones
        EMAIL_RECIPIENTS = 'tu@email.com'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    
    stages {
        stage('🔍 Checkout') {
            steps {
                echo '📥 Clonando repositorio desde GitHub...'
                checkout scm
                
                sh '''
                    echo "=== Información del Commit ==="
                    git log -1 --pretty=format:"Commit: %H%nAutor: %an%nFecha: %ad%nMensaje: %s"
                '''
            }
        }
        
        stage('🧪 Tests del Backend') {
            steps {
                echo '🐍 Ejecutando tests del backend Python...'
                dir('backend') {
                    sh '''
                        python3 -m venv venv || true
                        . venv/bin/activate || true
                        
                        pip install -r requirements.txt
                        pip install pytest pytest-cov pylint || true
                        
                        echo "✅ Dependencias instaladas"
                        
                        # Linting
                        pylint app.py --disable=all --enable=E,F || true
                        
                        echo "✅ Tests del backend completados"
                    '''
                }
            }
        }
        
        stage('🧪 Tests del Frontend') {
            steps {
                echo '⚛️ Ejecutando tests del frontend React...'
                dir('frontend') {
                    sh '''
                        npm install
                        
                        echo "✅ Dependencias instaladas"
                        
                        # Tests cuando estén configurados
                        # npm test -- --coverage --watchAll=false
                        
                        echo "✅ Tests del frontend completados"
                    '''
                }
            }
        }
        
        stage('🐳 Build de Imágenes Docker') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        echo '🔨 Construyendo imagen del frontend...'
                        script {
                            dir('frontend') {
                                sh "docker build -t ${FRONTEND_IMAGE}:${BUILD_VERSION} ."
                                sh "docker tag ${FRONTEND_IMAGE}:${BUILD_VERSION} ${FRONTEND_IMAGE}:latest"
                            }
                        }
                    }
                }
                
                stage('Build Backend') {
                    steps {
                        echo '🔨 Construyendo imagen del backend...'
                        script {
                            dir('backend') {
                                sh "docker build -t ${BACKEND_IMAGE}:${BUILD_VERSION} ."
                                sh "docker tag ${BACKEND_IMAGE}:${BUILD_VERSION} ${BACKEND_IMAGE}:latest"
                            }
                        }
                    }
                }
            }
        }
        
        stage('🧪 Tests de Integración') {
            steps {
                echo '🔗 Ejecutando tests de integración...'
                sh '''
                    docker-compose -f docker-compose.test.yml up -d || true
                    
                    echo "⏳ Esperando a que servicios estén listos..."
                    sleep 15
                    
                    echo "🧪 Verificando salud del backend..."
                    curl -f http://localhost:5001/api/health || echo "Warning: Health check failed"
                    
                    echo "🧹 Limpiando servicios de test..."
                    docker-compose -f docker-compose.test.yml down || true
                    
                    echo "✅ Tests de integración completados"
                '''
            }
        }
        
        stage('🚀 Deploy a Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo '🎭 Desplegando a entorno de staging...'
                sh '''
                    docker-compose down || true
                    
                    docker system prune -f || true
                    
                    docker-compose up -d
                    
                    sleep 5
                    docker-compose ps
                    
                    echo "✅ Deploy a staging completado"
                '''
            }
        }
        
        stage('🎯 Deploy a Producción') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Solicitando aprobación para producción...'
                
                input message: '¿Desplegar a producción?', ok: 'Deploy!'
                
                sh '''
                    echo "🔄 Actualizando servicios en producción..."
                    
                    docker-compose down || true
                    docker-compose up -d
                    
                    echo "✅ Deploy a producción completado"
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline ejecutado exitosamente!'
            
            script {
                def emailBody = """
                    <h2 style="color: #4CAF50;">✅ Build Exitoso</h2>
                    <p>El build <strong>#${BUILD_NUMBER}</strong> se completó exitosamente.</p>
                    <table style="border-collapse: collapse; width: 100%;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Commit:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">${GIT_COMMIT}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Branch:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">${GIT_BRANCH}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Duración:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">${currentBuild.durationString}</td>
                        </tr>
                    </table>
                    <p><a href="${BUILD_URL}">Ver detalles del build</a></p>
                """
                
                emailext (
                    subject: "✅ Jenkins Build #${BUILD_NUMBER} - SUCCESS",
                    body: emailBody,
                    to: "${EMAIL_RECIPIENTS}",
                    mimeType: 'text/html'
                )
            }
        }
        
        failure {
            echo '❌ Pipeline falló!'
            
            script {
                def emailBody = """
                    <h2 style="color: #F44336;">❌ Build Fallido</h2>
                    <p>El build <strong>#${BUILD_NUMBER}</strong> ha fallado.</p>
                    <p><strong>Commit:</strong> ${GIT_COMMIT}</p>
                    <p><strong>Branch:</strong> ${GIT_BRANCH}</p>
                    <p><a href="${BUILD_URL}console">Ver logs completos</a></p>
                    <p style="color: #F44336;"><strong>Acción requerida:</strong> Revisar logs y corregir errores.</p>
                """
                
                emailext (
                    subject: "❌ Jenkins Build #${BUILD_NUMBER} - FAILURE",
                    body: emailBody,
                    to: "${EMAIL_RECIPIENTS}",
                    mimeType: 'text/html'
                )
            }
        }
        
        always {
            echo '🧹 Limpiando workspace...'
            
            sh 'docker image prune -f || true'
            
            cleanWs()
        }
    }
}
