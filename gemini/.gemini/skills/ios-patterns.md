# iOS — Patterns & Idioms (Swift + SwiftUI)

Padroes e idiomas para iOS moderno em producao.

## Filosofia

- **SwiftUI-first**: UI declarativa, preview-driven
- **Structured Concurrency**: async/await, TaskGroup, actors
- **Observation framework**: @Observable (iOS 17+) substitui ObservableObject
- **SwiftData**: persistencia moderna (iOS 17+), alternativa a Core Data

## Estrutura de projeto

```
App/
├── App.swift                 # @main entry point
├── ContentView.swift
├── DI/                       # Dependency container
├── Data/
│   ├── Local/               # SwiftData/CoreData models
│   ├── Remote/              # API clients, DTOs
│   └── Repository/          # Repository implementations
├── Domain/
│   ├── Model/               # Domain models
│   ├── Repository/          # Repository protocols
│   └── UseCase/             # Use cases
├── UI/
│   ├── Theme/               # Colors, fonts, styles
│   ├── Components/          # Reusable views
│   ├── Navigation/          # Router, coordinator
│   └── Features/
│       └── Orders/
│           ├── OrderListView.swift
│           ├── OrderDetailView.swift
│           └── OrderViewModel.swift
└── Util/                    # Extensions, helpers
```

## SwiftUI Views

```swift
struct OrderListView: View {
    @State private var viewModel = OrderViewModel()

    var body: some View {
        NavigationStack {
            Group {
                switch viewModel.state {
                case .loading:
                    ProgressView()
                case .error(let message):
                    ErrorView(message: message, onRetry: { Task { await viewModel.refresh() } })
                case .loaded(let orders):
                    orderList(orders)
                }
            }
            .navigationTitle("Orders")
            .task { await viewModel.loadOrders() }
            .refreshable { await viewModel.refresh() }
        }
    }

    private func orderList(_ orders: [OrderUI]) -> some View {
        List(orders) { order in
            NavigationLink(value: order.id) {
                OrderRow(order: order)
            }
        }
        .navigationDestination(for: String.self) { id in
            OrderDetailView(orderId: id)
        }
    }
}

struct OrderRow: View {
    let order: OrderUI

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(order.title)
                .font(.headline)
            HStack {
                Text("Status: \(order.status)")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                Spacer()
                Text(order.formattedAmount)
                    .font(.subheadline)
                    .bold()
            }
        }
        .padding(.vertical, 4)
    }
}
```

## ViewModel (@Observable)

```swift
// iOS 17+ com Observation framework
@Observable
final class OrderViewModel {
    private let getOrdersUseCase: GetOrdersUseCase

    var state: ViewState<[OrderUI]> = .loading

    init(getOrdersUseCase: GetOrdersUseCase = .init()) {
        self.getOrdersUseCase = getOrdersUseCase
    }

    func loadOrders() async {
        state = .loading
        do {
            let orders = try await getOrdersUseCase.execute()
            state = .loaded(orders.map(\.toUI))
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    func refresh() async {
        await loadOrders()
    }
}

enum ViewState<T> {
    case loading
    case loaded(T)
    case error(String)
}

struct OrderUI: Identifiable {
    let id: String
    let title: String
    let status: String
    let formattedAmount: String
}
```

## Use Case

```swift
struct GetOrdersUseCase {
    private let repository: OrderRepository

    init(repository: OrderRepository = OrderRepositoryImpl()) {
        self.repository = repository
    }

    func execute(status: String? = nil) async throws -> [Order] {
        try await repository.getOrders(status: status)
    }
}
```

## Repository

```swift
// Domain layer — protocol
protocol OrderRepository {
    func getOrders(status: String?) async throws -> [Order]
    func getOrder(id: String) async throws -> Order
    func createOrder(_ request: CreateOrderRequest) async throws -> Order
}

// Data layer — implementation
final class OrderRepositoryImpl: OrderRepository {
    private let apiClient: OrderAPIClient
    private let localStore: OrderLocalStore

    init(apiClient: OrderAPIClient = .init(), localStore: OrderLocalStore = .init()) {
        self.apiClient = apiClient
        self.localStore = localStore
    }

    func getOrders(status: String?) async throws -> [Order] {
        let dtos = try await apiClient.getOrders(status: status)
        let orders = dtos.map(\.toDomain)
        await localStore.save(orders)
        return orders
    }

    func getOrder(id: String) async throws -> Order {
        try await apiClient.getOrder(id: id).toDomain
    }

    func createOrder(_ request: CreateOrderRequest) async throws -> Order {
        let dto = try await apiClient.createOrder(request.toDTO)
        let order = dto.toDomain
        await localStore.save([order])
        return order
    }
}
```

## API Client (URLSession)

```swift
final class OrderAPIClient {
    private let baseURL: URL
    private let session: URLSession
    private let decoder: JSONDecoder

    init(baseURL: URL = Config.apiBaseURL, session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601
    }

    func getOrders(status: String? = nil) async throws -> [OrderDTO] {
        var components = URLComponents(url: baseURL.appending(path: "api/v1/orders"), resolvingAgainstBaseURL: false)!
        if let status { components.queryItems = [URLQueryItem(name: "status", value: status)] }
        return try await request(url: components.url!)
    }

    func createOrder(_ dto: CreateOrderDTO) async throws -> OrderDTO {
        var urlRequest = URLRequest(url: baseURL.appending(path: "api/v1/orders"))
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.httpBody = try JSONEncoder().encode(dto)
        return try await request(urlRequest: urlRequest)
    }

    private func request<T: Decodable>(url: URL) async throws -> T {
        let (data, response) = try await session.data(from: url)
        try validateResponse(response)
        return try decoder.decode(T.self, from: data)
    }

    private func request<T: Decodable>(urlRequest: URLRequest) async throws -> T {
        let (data, response) = try await session.data(for: urlRequest)
        try validateResponse(response)
        return try decoder.decode(T.self, from: data)
    }

    private func validateResponse(_ response: URLResponse) throws {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.httpError(statusCode: httpResponse.statusCode)
        }
    }
}

enum APIError: LocalizedError {
    case invalidResponse
    case httpError(statusCode: Int)

    var errorDescription: String? {
        switch self {
        case .invalidResponse: "Invalid response"
        case .httpError(let code): "HTTP error: \(code)"
        }
    }
}
```

## SwiftData (iOS 17+)

```swift
@Model
final class OrderLocal {
    @Attribute(.unique) var id: String
    var title: String
    var amount: Double
    var status: String
    var createdAt: Date

    init(id: String, title: String, amount: Double, status: String, createdAt: Date) {
        self.id = id
        self.title = title
        self.amount = amount
        self.status = status
        self.createdAt = createdAt
    }
}

// App.swift
@main
struct OrderApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: OrderLocal.self)
    }
}

// Actor-based local store
actor OrderLocalStore {
    private let container: ModelContainer

    init() {
        self.container = try! ModelContainer(for: OrderLocal.self)
    }

    func save(_ orders: [Order]) {
        let context = ModelContext(container)
        for order in orders {
            context.insert(order.toLocal)
        }
        try? context.save()
    }
}
```

## Navigation (Router)

```swift
@Observable
final class AppRouter {
    var path = NavigationPath()

    func navigate(to destination: Destination) {
        path.append(destination)
    }

    func goBack() {
        path.removeLast()
    }

    func goToRoot() {
        path.removeLast(path.count)
    }
}

enum Destination: Hashable {
    case orderDetail(id: String)
    case createOrder
}
```

## Testing

```swift
// ViewModel test
@Test func loadOrdersSuccess() async {
    let mockRepo = MockOrderRepository()
    mockRepo.orders = [Order(id: "1", title: "Test", amount: 99, status: "pending")]
    let useCase = GetOrdersUseCase(repository: mockRepo)
    let viewModel = OrderViewModel(getOrdersUseCase: useCase)

    await viewModel.loadOrders()

    guard case .loaded(let orders) = viewModel.state else {
        Issue.record("Expected loaded state"); return
    }
    #expect(orders.count == 1)
    #expect(orders.first?.title == "Test")
}

// View snapshot test (with swift-snapshot-testing)
@Test func orderRowSnapshot() {
    let order = OrderUI(id: "1", title: "Order 1", status: "pending", formattedAmount: "$99.00")
    let view = OrderRow(order: order).frame(width: 375)
    assertSnapshot(of: view, as: .image)
}

// UI test
func testOrderListDisplaysOrders() throws {
    let app = XCUIApplication()
    app.launch()
    XCTAssertTrue(app.staticTexts["Orders"].exists)
    XCTAssertTrue(app.cells.count > 0)
}
```

## Checklist

- [ ] SwiftUI para toda UI nova?
- [ ] @Observable (iOS 17+) para ViewModels (nao ObservableObject)?
- [ ] async/await para concorrencia (nao callbacks/closures)?
- [ ] Structured concurrency (Task, TaskGroup)?
- [ ] Repository pattern (protocol + implementation)?
- [ ] SwiftData para persistencia local (iOS 17+)?
- [ ] Navigation com NavigationStack + NavigationPath?
- [ ] Error handling com typed errors?
- [ ] Testes unitarios com Swift Testing (@Test)?
- [ ] Preview para cada view significativa?
- [ ] Keychain para dados sensiveis (nao UserDefaults)?
