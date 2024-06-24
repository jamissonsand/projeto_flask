from flask import Flask, request, send_file
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import io

app = Flask(__name__)

@app.route('/api/plot', methods=['GET'])
def plot_with_image_and_background():
    # Obter parâmetros de consulta
    x = float(request.args.get('x', 5))
    y = float(request.args.get('y', 8))

    # Carregar imagens
    background_path = 'static/background.png'
    point_image_path = 'static/round-point.png'

    # Configurar o gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Carregar a imagem de fundo
    bg_img = mpimg.imread(background_path)
    ax.imshow(bg_img, extent=[-13, 13, 0, 12], aspect='auto')

    # Definir os limites dos eixos
    ax.set_xlim(-13, 13)
    ax.set_ylim(0, 12)
    
    # Configurar o grid
    ax.set_xticks(range(-13, 14, 1))
    ax.set_yticks(range(0, 13, 2))
    ax.grid(True, which='both', color='white', linestyle='--', linewidth=0.5)  # Grid branco para visibilidade sobre o fundo
    
    # Remover os rótulos dos eixos
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Carregar a imagem do ponto
    point_img = mpimg.imread(point_image_path)
    imagebox = OffsetImage(point_img, zoom=1)  # Ajuste o zoom conforme necessário
    
    # Adicionar a imagem no ponto especificado
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)
    
    # Remover os títulos dos eixos
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Ajustar o layout para remover margens extras
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # Criar um buffer para salvar a imagem
    img_buffer = io.BytesIO()
    
    # Salvar a imagem no buffer
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # Retornar a imagem gerada como resposta
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)