IF OBJECT_ID (N'select_orders_by_item_name', N'IF') IS NOT NULL  
    DROP FUNCTION select_orders_by_item_name;
		 
GO  

CREATE FUNCTION select_orders_by_item_name(@name_item nvarchar(20))  
RETURNS TABLE  
AS    
RETURN
(
	SELECT Orders.row_id, Customers.name, COUNT(Orders.row_id) AS 'Count Item'
	FROM Orders 
	JOIN OrderItems ON OrderItems.order_id = Orders.row_id 
	JOIN Customers ON Orders.customer_id = Customers.row_id
	WHERE OrderItems.name = @name_item
	GROUP BY Orders.row_id, Customers.name
);

GO

SELECT * FROM select_orders_by_item_name(N'Кассовый аппарат');

GO

-- Задание 2

IF OBJECT_ID (N'calculate_total_price_for_orders_group', N'FN') IS NOT NULL  
    DROP FUNCTION calculate_total_price_for_orders_group;

GO

CREATE FUNCTION calculate_total_price_for_orders_group(@group_id int)
RETURNS int   
AS
BEGIN 
    DECLARE @group nvarchar(20), @total_price int;
    SET @group = 
	(
		SELECT group_name
		FROM Orders 
		WHERE row_id = @group_id
	);

	IF @group IS NULL
        SELECT @total_price = SUM(OrderItems.price)
        FROM OrderItems
        WHERE OrderItems.order_id = @group_id;
    ELSE
        WITH
		Node(row_id, parent_id, group_name) 
		AS 
		(
            SELECT row_id, parent_id, group_name
            FROM Orders
            WHERE parent_id = @group_id
            UNION ALL
            SELECT d.row_id, d.parent_id, d.group_name
            FROM orders d
            JOIN Node ON Node.row_id = d.parent_id
		)

        SELECT @total_price = SUM(price)
		FROM Node
        JOIN OrderItems ON OrderItems.order_id = Node.row_id
        WHERE Node.group_name IS NULL;
        RETURN @total_price;
END; 

GO 

SELECT dbo.calculate_total_price_for_orders_group(3) AS 'total_price';

GO


-- Задание 3

SELECT Customers.name
FROM Customers
JOIN Orders ON Orders.customer_id = Customers.row_id
JOIN OrderItems ON Orders.row_id = OrderItems.order_id
WHERE YEAR (Orders.registered_at) = 2020
GROUP BY Customers.name, Customers.row_id
HAVING COUNT(DISTINCT OrderItems.order_id) = COUNT(DISTINCT CASE WHEN OrderItems.name = 'Кассовый аппарат' THEN OrderItems.order_id END);
