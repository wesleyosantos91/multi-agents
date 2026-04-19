---
name: android-patterns
description: "Padrões Android modernos: Kotlin, Jetpack Compose, MVVM, Hilt, Room, Navigation, Coroutines, testes. Use quando implementar features em Android nativo."
argument-hint: "[contexto adicional]"
---

# Android — Patterns & Idioms (Kotlin + Jetpack Compose)

Padroes e idiomas para Android moderno em producao.

## Filosofia

- **Compose-first**: UI declarativa, sem XML layouts
- **Unidirectional Data Flow (UDF)**: State desce, Events sobem
- **Hilt para DI**: injecao de dependencia com suporte a lifecycle
- **Coroutines + Flow**: concorrencia idiomatica Kotlin

## Estrutura de projeto

```
app/src/main/java/com/example/app/
├── di/                    # Hilt modules
├── data/
│   ├── local/            # Room (entities, DAOs, database)
│   ├── remote/           # Retrofit (API interfaces, DTOs)
│   └── repository/       # Repository implementations
├── domain/
│   ├── model/            # Domain models
│   ├── repository/       # Repository interfaces
│   └── usecase/          # Use cases
├── ui/
│   ├── theme/            # Material Theme, colors, typography
│   ├── components/       # Composables reutilizaveis
│   ├── navigation/       # NavHost, routes
│   └── features/
│       └── orders/
│           ├── OrderListScreen.kt
│           ├── OrderDetailScreen.kt
│           └── OrderViewModel.kt
├── util/                 # Extensions, helpers
└── App.kt               # Application class (@HiltAndroidApp)
```

## Compose UI

```kotlin
@Composable
fun OrderListScreen(
    viewModel: OrderViewModel = hiltViewModel(),
    onOrderClick: (String) -> Unit,
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Orders") }) },
    ) { padding ->
        when (val state = uiState) {
            is OrderUiState.Loading -> LoadingIndicator(Modifier.padding(padding))
            is OrderUiState.Error -> ErrorMessage(state.message, onRetry = viewModel::refresh)
            is OrderUiState.Success -> OrderList(
                orders = state.orders,
                onOrderClick = onOrderClick,
                modifier = Modifier.padding(padding),
            )
        }
    }
}

@Composable
private fun OrderList(
    orders: List<OrderUi>,
    onOrderClick: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    LazyColumn(modifier = modifier) {
        items(orders, key = { it.id }) { order ->
            OrderCard(order = order, onClick = { onOrderClick(order.id) })
        }
    }
}

@Composable
private fun OrderCard(order: OrderUi, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = order.title, style = MaterialTheme.typography.titleMedium)
            Text(text = "Status: ${order.status}", style = MaterialTheme.typography.bodyMedium)
            Text(text = order.formattedAmount, style = MaterialTheme.typography.bodySmall)
        }
    }
}
```

## ViewModel (UDF)

```kotlin
@HiltViewModel
class OrderViewModel @Inject constructor(
    private val getOrdersUseCase: GetOrdersUseCase,
) : ViewModel() {

    private val _uiState = MutableStateFlow<OrderUiState>(OrderUiState.Loading)
    val uiState: StateFlow<OrderUiState> = _uiState.asStateFlow()

    init { refresh() }

    fun refresh() {
        viewModelScope.launch {
            _uiState.value = OrderUiState.Loading
            getOrdersUseCase()
                .catch { e -> _uiState.value = OrderUiState.Error(e.message ?: "Unknown error") }
                .collect { orders -> _uiState.value = OrderUiState.Success(orders.map { it.toUi() }) }
        }
    }
}

sealed interface OrderUiState {
    data object Loading : OrderUiState
    data class Success(val orders: List<OrderUi>) : OrderUiState
    data class Error(val message: String) : OrderUiState
}

data class OrderUi(
    val id: String,
    val title: String,
    val status: String,
    val formattedAmount: String,
)
```

## Use Case

```kotlin
class GetOrdersUseCase @Inject constructor(
    private val repository: OrderRepository,
) {
    operator fun invoke(): Flow<List<Order>> = repository.getOrders()
}
```

## Repository

```kotlin
// Domain layer — interface
interface OrderRepository {
    fun getOrders(): Flow<List<Order>>
    suspend fun getOrder(id: String): Order
    suspend fun createOrder(request: CreateOrderRequest): Order
}

// Data layer — implementation
class OrderRepositoryImpl @Inject constructor(
    private val api: OrderApi,
    private val dao: OrderDao,
) : OrderRepository {

    override fun getOrders(): Flow<List<Order>> {
        return dao.observeAll().map { entities -> entities.map { it.toDomain() } }
    }

    override suspend fun getOrder(id: String): Order {
        return api.getOrder(id).toDomain()
    }

    override suspend fun createOrder(request: CreateOrderRequest): Order {
        val response = api.createOrder(request.toDto())
        dao.insert(response.toEntity())
        return response.toDomain()
    }
}
```

## Room (Local)

```kotlin
@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    val title: String,
    val amount: Double,
    val status: String,
    @ColumnInfo(name = "created_at") val createdAt: Long,
)

@Dao
interface OrderDao {
    @Query("SELECT * FROM orders ORDER BY created_at DESC")
    fun observeAll(): Flow<List<OrderEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(order: OrderEntity)

    @Query("DELETE FROM orders WHERE id = :id")
    suspend fun deleteById(id: String)
}

@Database(entities = [OrderEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun orderDao(): OrderDao
}
```

## Retrofit (Remote)

```kotlin
interface OrderApi {
    @GET("api/v1/orders")
    suspend fun getOrders(@Query("status") status: String? = null): List<OrderDto>

    @GET("api/v1/orders/{id}")
    suspend fun getOrder(@Path("id") id: String): OrderDto

    @POST("api/v1/orders")
    suspend fun createOrder(@Body request: CreateOrderDto): OrderDto
}
```

## Hilt DI

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .addConverterFactory(MoshiConverterFactory.create())
        .client(OkHttpClient.Builder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .addInterceptor(AuthInterceptor())
            .build())
        .build()

    @Provides @Singleton
    fun provideOrderApi(retrofit: Retrofit): OrderApi = retrofit.create(OrderApi::class.java)
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase =
        Room.databaseBuilder(context, AppDatabase::class.java, "app.db").build()

    @Provides
    fun provideOrderDao(db: AppDatabase): OrderDao = db.orderDao()
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds @Singleton
    abstract fun bindOrderRepository(impl: OrderRepositoryImpl): OrderRepository
}
```

## Navigation (Compose)

```kotlin
@Composable
fun AppNavHost(navController: NavHostController = rememberNavController()) {
    NavHost(navController = navController, startDestination = "orders") {
        composable("orders") {
            OrderListScreen(onOrderClick = { id -> navController.navigate("orders/$id") })
        }
        composable("orders/{id}", arguments = listOf(navArgument("id") { type = NavType.StringType })) {
            OrderDetailScreen(onBack = { navController.popBackStack() })
        }
    }
}
```

## Testing

```kotlin
// ViewModel test
@Test
fun `should load orders successfully`() = runTest {
    val orders = listOf(Order("1", "Test", 99.0, "pending"))
    coEvery { getOrdersUseCase() } returns flowOf(orders)

    val viewModel = OrderViewModel(getOrdersUseCase)

    viewModel.uiState.test {
        assertThat(awaitItem()).isInstanceOf(OrderUiState.Loading::class.java)
        val success = awaitItem() as OrderUiState.Success
        assertThat(success.orders).hasSize(1)
    }
}

// Compose UI test
@get:Rule val composeTestRule = createComposeRule()

@Test
fun `should display order list`() {
    composeTestRule.setContent {
        OrderList(orders = listOf(OrderUi("1", "Order 1", "pending", "$99.00")), onOrderClick = {})
    }
    composeTestRule.onNodeWithText("Order 1").assertIsDisplayed()
    composeTestRule.onNodeWithText("Status: pending").assertIsDisplayed()
}
```

## Checklist

- [ ] Compose para toda UI nova (nao XML)?
- [ ] ViewModel com UDF (StateFlow, sealed interface)?
- [ ] collectAsStateWithLifecycle (nao collectAsState)?
- [ ] Hilt para DI (@HiltViewModel, @Inject)?
- [ ] Room para cache local com Flow?
- [ ] Retrofit com coroutines (suspend)?
- [ ] Repository pattern (domain interface, data impl)?
- [ ] Navigation Compose?
- [ ] Testes de ViewModel com Turbine?
- [ ] Testes de UI com ComposeTestRule?
- [ ] ProGuard/R8 rules para release?
