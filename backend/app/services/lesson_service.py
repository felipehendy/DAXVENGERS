"""
Serviço para gerenciar lições e conteúdo do jogo
"""

from typing import List, Optional, Dict
from app.models.lesson import Lesson, Mission, Exercise, ExerciseType, LessonType


class LessonService:
    """Serviço para gerenciar lições"""
    
    def __init__(self):
        """Inicializa o serviço com conteúdo de exemplo"""
        self.lessons_db = self._load_initial_content()
        self.missions_db = self._load_missions()
    
    def _load_missions(self) -> Dict[str, Mission]:
        """Carrega missões disponíveis"""
        return {
            "dax-basics": Mission(
                id="dax-basics",
                name="Funções Básicas DAX",
                icon="🦾",
                description="Domine as funções essenciais do DAX como um verdadeiro Vingador",
                total_lessons=5,
                total_xp=320,
                is_free=True,
                order=1,
                badge_reward="Iron Man"
            ),
            "power-query": Mission(
                id="power-query",
                name="Power Query Master",
                icon="🔗",
                description="Transforme dados como o Homem de Ferro monta sua armadura",
                total_lessons=8,
                total_xp=560,
                is_free=True,
                order=2,
                badge_reward="War Machine"
            ),
            "dax-advanced": Mission(
                id="dax-advanced",
                name="DAX Avançado",
                icon="⚡",
                description="Domine técnicas avançadas e se torne um Vingador supremo",
                total_lessons=10,
                total_xp=900,
                is_free=False,
                order=3,
                badge_reward="Thor"
            )
        }
    
    def _load_initial_content(self) -> Dict[int, Lesson]:
        """Carrega conteúdo inicial das lições"""
        
        lessons = {
            # LIÇÃO 1: Introdução ao DAX
            1: Lesson(
                id=1,
                title="Introdução ao DAX",
                icon="📊",
                description="Aprenda o que é DAX e por que ele é essencial",
                xp=50,
                type=LessonType.THEORY,
                mission_id="dax-basics",
                order=1,
                theory="""
                    <h3>📚 O que é DAX?</h3>
                    <p>DAX (Data Analysis Expressions) é a linguagem de fórmulas do Power BI. É como o Excel, mas MUITO mais poderoso!</p>
                    
                    <p><strong>Por que aprender DAX?</strong></p>
                    <ul>
                        <li>✅ Criar KPIs e métricas complexas</li>
                        <li>✅ Análises dinâmicas que mudam com filtros</li>
                        <li>✅ Dashboards profissionais impressionantes</li>
                        <li>✅ Alta demanda no mercado 💰</li>
                    </ul>

                    <pre><code>// Exemplo de medida DAX simples
Total Vendas = SUM(Vendas[Valor])</code></pre>

                    <p>💡 <strong>Dica Ninja:</strong> DAX calcula em tempo real! Diferente de colunas calculadas que são fixas.</p>
                """,
                key_concepts=["DAX", "Medidas", "Análise de dados"],
                exercises=[
                    Exercise(
                        type=ExerciseType.MULTIPLE_CHOICE,
                        question="O que significa DAX?",
                        options=[
                            "Data Analysis Expressions",
                            "Database Analysis eXcel",
                            "Dynamic Analysis X-ray",
                            "Data Advanced eXcel"
                        ],
                        correct=0,
                        explanation="DAX = Data Analysis Expressions. É a linguagem de fórmulas criada pela Microsoft para Power BI!"
                    )
                ],
                estimated_time=5
            ),
            
            # LIÇÃO 2: Função SUM
            2: Lesson(
                id=2,
                title="Função SUM",
                icon="➕",
                description="Domine a função mais básica e essencial",
                xp=60,
                type=LessonType.PRACTICE,
                mission_id="dax-basics",
                order=2,
                theory="""
                    <h3>➕ Dominando a Função SUM</h3>
                    <p>SUM é a função mais básica e essencial do DAX. Ela soma todos os valores de uma coluna.</p>
                    
                    <p><strong>Sintaxe:</strong></p>
                    <pre><code>SUM(&lt;coluna&gt;)</code></pre>

                    <p><strong>Exemplos Reais:</strong></p>
                    <pre><code>Total Vendas = SUM(Vendas[Valor])

Total Quantidade = SUM(Vendas[Quantidade])

Custo Total = SUM(Produtos[Custo])</code></pre>

                    <p>⚠️ <strong>Importante:</strong> SUM só funciona com colunas numéricas!</p>

                    <p>💡 <strong>Quando usar:</strong> Sempre que precisar somar valores totais: vendas, custos, quantidades, etc.</p>
                """,
                key_concepts=["SUM", "Agregação", "Medidas básicas"],
                exercises=[
                    Exercise(
                        type=ExerciseType.CODE,
                        question="Crie uma medida chamada 'Receita Total' que soma a coluna Receita da tabela Financeiro:",
                        solution="Receita Total = SUM(Financeiro[Receita])",
                        hints=[
                            "Use a função SUM",
                            "Formato: NomeMedida = SUM(Tabela[Coluna])",
                            "Resposta: Receita Total = SUM(Financeiro[Receita])"
                        ],
                        explanation="Perfeito! Você criou sua primeira medida DAX!"
                    )
                ],
                estimated_time=4,
                prerequisites=[1]
            ),
            
            # LIÇÃO 3: Função AVERAGE
            3: Lesson(
                id=3,
                title="Função AVERAGE",
                icon="📈",
                description="Calcule médias com precisão",
                xp=60,
                type=LessonType.PRACTICE,
                mission_id="dax-basics",
                order=3,
                theory="""
                    <h3>📈 Calculando Médias com AVERAGE</h3>
                    <p>AVERAGE calcula a média aritmética dos valores de uma coluna (ignorando valores em branco).</p>
                    
                    <p><strong>Sintaxe:</strong></p>
                    <pre><code>AVERAGE(&lt;coluna&gt;)</code></pre>

                    <p><strong>Exemplos Práticos:</strong></p>
                    <pre><code>Ticket Médio = AVERAGE(Vendas[Valor])

Idade Média = AVERAGE(Clientes[Idade])

Avaliação Média = AVERAGE(Feedback[Nota])</code></pre>

                    <p>🎯 <strong>Diferença importante:</strong></p>
                    <p>• AVERAGE ignora células vazias<br>
                    • Se quiser incluir zeros, use AVERAGEX</p>

                    <p>💡 <strong>Caso real:</strong> Use para calcular ticket médio de vendas, nota média de avaliações.</p>
                """,
                key_concepts=["AVERAGE", "Médias", "Agregação"],
                exercises=[
                    Exercise(
                        type=ExerciseType.MULTIPLE_CHOICE,
                        question="AVERAGE ignora células vazias?",
                        options=[
                            "Sim, ignora células vazias",
                            "Não, considera como zero",
                            "Depende da versão do Power BI",
                            "Só ignora se você configurar"
                        ],
                        correct=0,
                        explanation="AVERAGE automaticamente ignora células vazias no cálculo!"
                    )
                ],
                estimated_time=4,
                prerequisites=[2]
            ),
            
            # LIÇÃO 4: Função COUNT
            4: Lesson(
                id=4,
                title="Função COUNT",
                icon="🔢",
                description="Conte elementos como um profissional",
                xp=70,
                type=LessonType.PRACTICE,
                mission_id="dax-basics",
                order=4,
                theory="""
                    <h3>🔢 Contando com COUNT e COUNTROWS</h3>
                    <p>Existem duas funções principais para contar no DAX:</p>
                    
                    <p><strong>COUNT - Conta valores não vazios em uma coluna:</strong></p>
                    <pre><code>Produtos Vendidos = COUNT(Vendas[Produto])</code></pre>

                    <p><strong>COUNTROWS - Conta linhas de uma tabela:</strong></p>
                    <pre><code>Total Vendas = COUNTROWS(Vendas)

Num Clientes = COUNTROWS(Clientes)</code></pre>

                    <p>⚡ <strong>Qual usar?</strong></p>
                    <p>• COUNT: Para contar valores em uma coluna específica<br>
                    • COUNTROWS: Para contar total de linhas da tabela</p>

                    <p>💡 <strong>Dica Pro:</strong> COUNTROWS geralmente é mais rápido e confiável!</p>
                """,
                key_concepts=["COUNT", "COUNTROWS", "Contagem"],
                exercises=[
                    Exercise(
                        type=ExerciseType.CODE,
                        question="Crie uma medida 'Quantidade Pedidos' que conta o número de linhas da tabela Pedidos:",
                        solution="Quantidade Pedidos = COUNTROWS(Pedidos)",
                        hints=[
                            "Use COUNTROWS para contar linhas",
                            "Formato: NomeMedida = COUNTROWS(Tabela)",
                            "Resposta: Quantidade Pedidos = COUNTROWS(Pedidos)"
                        ],
                        explanation="Excelente! COUNTROWS é perfeito para contar linhas!"
                    )
                ],
                estimated_time=5,
                prerequisites=[3]
            ),
            
            # LIÇÃO 5: Função CALCULATE
            5: Lesson(
                id=5,
                title="Função CALCULATE",
                icon="⚡",
                description="A função mais poderosa do DAX",
                xp=80,
                type=LessonType.CHALLENGE,
                mission_id="dax-basics",
                order=5,
                theory="""
                    <h3>⚡ CALCULATE - A Função Mais Poderosa do DAX</h3>
                    <p>CALCULATE é responsável por 70% de todas as medidas avançadas! Ela modifica o contexto de filtro.</p>
                    
                    <p><strong>Sintaxe:</strong></p>
                    <pre><code>CALCULATE(&lt;expressão&gt;, &lt;filtro1&gt;, &lt;filtro2&gt;, ...)</code></pre>

                    <p><strong>Pense assim:</strong> CALCULATE é como colocar um filtro temporário nos dados!</p>

                    <p><strong>Exemplos Essenciais:</strong></p>
                    <pre><code>// Vendas apenas de São Paulo
Vendas SP = CALCULATE(
    SUM(Vendas[Valor]),
    Vendas[Estado] = "SP"
)

// Vendas acima de R$ 1000
Vendas Alto Valor = CALCULATE(
    SUM(Vendas[Valor]),
    Vendas[Valor] > 1000
)</code></pre>

                    <p>💎 <strong>Pro Tip:</strong> Você pode combinar múltiplos filtros!</p>

                    <p>🎯 <strong>Use quando:</strong> Precisar filtrar dados dinamicamente, criar KPIs segmentados.</p>
                """,
                key_concepts=["CALCULATE", "Contexto de filtro", "Filtros dinâmicos"],
                exercises=[
                    Exercise(
                        type=ExerciseType.CODE,
                        question="Crie uma medida 'Vendas RJ' que soma vendas apenas do Rio de Janeiro:",
                        solution='Vendas RJ = CALCULATE(SUM(Vendas[Valor]), Vendas[Estado] = "RJ")',
                        hints=[
                            "Use CALCULATE com SUM dentro",
                            'O filtro é: Vendas[Estado] = "RJ"',
                            'Resposta: Vendas RJ = CALCULATE(SUM(Vendas[Valor]), Vendas[Estado] = "RJ")'
                        ],
                        explanation="Perfeito! Você dominou CALCULATE, a função mais importante do DAX!"
                    )
                ],
                estimated_time=6,
                prerequisites=[4]
            )
        }
        
        return lessons
    
    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Retorna uma missão específica"""
        return self.missions_db.get(mission_id)
    
    def get_all_missions(self) -> List[Mission]:
        """Retorna todas as missões"""
        return sorted(self.missions_db.values(), key=lambda m: m.order)
    
    def get_lessons_by_mission(self, mission_id: str) -> List[Lesson]:
        """Retorna todas as lições de uma missão"""
        lessons = [
            lesson for lesson in self.lessons_db.values()
            if lesson.mission_id == mission_id
        ]
        return sorted(lessons, key=lambda l: l.order)
    
    def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        """Retorna uma lição específica"""
        return self.lessons_db.get(lesson_id)
    
    def get_next_lesson(self, current_lesson_id: int, mission_id: str) -> Optional[Lesson]:
        """Retorna a próxima lição da missão"""
        lessons = self.get_lessons_by_mission(mission_id)
        for i, lesson in enumerate(lessons):
            if lesson.id == current_lesson_id and i < len(lessons) - 1:
                return lessons[i + 1]
        return None


# Singleton instance
lesson_service = LessonService()