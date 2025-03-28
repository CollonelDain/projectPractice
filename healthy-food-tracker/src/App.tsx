import { useState } from 'react';
import { Container, Navbar, Nav, Row, Col, Card, Form, Button, Table, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

type Meal = {
  id: string;
  name: string;
  calories: number;
  proteins: number;
  carbs: number;
  fats: number;
  date: string;
};

type DailyStats = {
  totalCalories: number;
  totalProteins: number;
  totalCarbs: number;
  totalFats: number;
};

export default function App() {
  const [meals, setMeals] = useState<Meal[]>([]);
  const [newMeal, setNewMeal] = useState<Omit<Meal, 'id' | 'date'>>({ 
    name: '', 
    calories: 0, 
    proteins: 0, 
    carbs: 0, 
    fats: 0 
  });
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [activeTab, setActiveTab] = useState<'today' | 'history'>('today');

  const dailyStats: DailyStats = meals.reduce((acc, meal) => {
    if (meal.date === date) {
      acc.totalCalories += meal.calories;
      acc.totalProteins += meal.proteins;
      acc.totalCarbs += meal.carbs;
      acc.totalFats += meal.fats;
    }
    return acc;
  }, { totalCalories: 0, totalProteins: 0, totalCarbs: 0, totalFats: 0 });

  const handleAddMeal = () => {
    if (!newMeal.name) return;

    const meal: Meal = {
      id: Date.now().toString(),
      ...newMeal,
      date: date
    };

    setMeals([...meals, meal]);
    setNewMeal({ name: '', calories: 0, proteins: 0, carbs: 0, fats: 0 });
  };

  const handleDeleteMeal = (id: string) => {
    setMeals(meals.filter(meal => meal.id !== id));
  };

  return (
    <div className="App">
      <Navbar bg="success" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="#">Трекер здорового питания</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link active={activeTab === 'today'} onClick={() => setActiveTab('today')}>Сегодня</Nav.Link>
              <Nav.Link active={activeTab === 'history'} onClick={() => setActiveTab('history')}>История</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container>
        {activeTab === 'today' ? (
          <>
            <Row className="mb-4">
              <Col>
                <Card>
                  <Card.Header>Дневная статистика</Card.Header>
                  <Card.Body>
                    <Row>
                      <Col>
                        <Card.Text><strong>Калории:</strong> {dailyStats.totalCalories} ккал</Card.Text>
                        <Card.Text><strong>Белки:</strong> {dailyStats.totalProteins} г</Card.Text>
                      </Col>
                      <Col>
                        <Card.Text><strong>Углеводы:</strong> {dailyStats.totalCarbs} г</Card.Text>
                        <Card.Text><strong>Жиры:</strong> {dailyStats.totalFats} г</Card.Text>
                      </Col>
                    </Row>
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            <Row className="mb-4">
              <Col>
                <Card>
                  <Card.Header>Добавить прием пищи</Card.Header>
                  <Card.Body>
                    <Form>
                      <Row className="mb-3">
                        <Col md={3}>
                          <Form.Group controlId="formDate">
                            <Form.Label>Дата</Form.Label>
                            <Form.Control 
                              type="date" 
                              value={date}
                              onChange={(e) => setDate(e.target.value)}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group controlId="formMealName">
                            <Form.Label>Название</Form.Label>
                            <Form.Control 
                              type="text" 
                              placeholder="Завтрак, Обед и т.д." 
                              value={newMeal.name}
                              onChange={(e) => setNewMeal({...newMeal, name: e.target.value})}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={2}>
                          <Form.Group controlId="formCalories">
                            <Form.Label>Калории (ккал)</Form.Label>
                            <Form.Control 
                              type="number" 
                              value={newMeal.calories}
                              onChange={(e) => setNewMeal({...newMeal, calories: +e.target.value})}
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Row className="mb-3">
                        <Col md={3}>
                          <Form.Group controlId="formProteins">
                            <Form.Label>Белки (г)</Form.Label>
                            <Form.Control 
                              type="number" 
                              value={newMeal.proteins}
                              onChange={(e) => setNewMeal({...newMeal, proteins: +e.target.value})}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group controlId="formCarbs">
                            <Form.Label>Углеводы (г)</Form.Label>
                            <Form.Control 
                              type="number" 
                              value={newMeal.carbs}
                              onChange={(e) => setNewMeal({...newMeal, carbs: +e.target.value})}
                            />
                          </Form.Group>
                        </Col>
                        <Col md={3}>
                          <Form.Group controlId="formFats">
                            <Form.Label>Жиры (г)</Form.Label>
                            <Form.Control 
                              type="number" 
                              value={newMeal.fats}
                              onChange={(e) => setNewMeal({...newMeal, fats: +e.target.value})}
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                      <Button variant="success" onClick={handleAddMeal}>
                        Добавить прием пищи
                      </Button>
                    </Form>
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            <Row>
              <Col>
                <Card>
                  <Card.Header>Сегодняшние приемы пищи</Card.Header>
                  <Card.Body>
                    {meals.filter(meal => meal.date === date).length === 0 ? (
                      <Alert variant="info">Сегодня еще не было добавлено приемов пищи</Alert>
                    ) : (
                      <Table striped bordered hover>
                        <thead>
                          <tr>
                            <th>Название</th>
                            <th>Калории</th>
                            <th>Белки</th>
                            <th>Углеводы</th>
                            <th>Жиры</th>
                            <th>Действия</th>
                          </tr>
                        </thead>
                        <tbody>
                          {meals
                            .filter(meal => meal.date === date)
                            .map(meal => (
                              <tr key={meal.id}>
                                <td>{meal.name}</td>
                                <td>{meal.calories} ккал</td>
                                <td>{meal.proteins} г</td>
                                <td>{meal.carbs} г</td>
                                <td>{meal.fats} г</td>
                                <td>
                                  <Button 
                                    variant="danger" 
                                    size="sm"
                                    onClick={() => handleDeleteMeal(meal.id)}
                                  >
                                    Удалить
                                  </Button>
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </Table>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            </Row>
          </>
        ) : (
          <Row>
            <Col>
              <Card>
                <Card.Header>История питания</Card.Header>
                <Card.Body>
                  {meals.length === 0 ? (
                    <Alert variant="info">Нет данных о приемах пищи</Alert>
                  ) : (
                    <Table striped bordered hover>
                      <thead>
                        <tr>
                          <th>Дата</th>
                          <th>Прием пищи</th>
                          <th>Калории</th>
                          <th>Белки</th>
                          <th>Углеводы</th>
                          <th>Жиры</th>
                        </tr>
                      </thead>
                      <tbody>
                        {meals.map(meal => (
                          <tr key={meal.id}>
                            <td>{meal.date}</td>
                            <td>{meal.name}</td>
                            <td>{meal.calories} ккал</td>
                            <td>{meal.proteins} г</td>
                            <td>{meal.carbs} г</td>
                            <td>{meal.fats} г</td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
}