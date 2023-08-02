<div class="guide-content">
	<p>Для создания шаблона договора необходимо:</p>
	<ol>
		<li>
			Создать документ в формате <b>docx</b> с помощью Microsoft Word или аналогичной программы.
		</li>
		<li>В документе можно указать поля, которые будут заменены на введенные значения.</li>
		<li>
			Поля должны быть в формате <nobr><b>&lbrace;&lbrace; field_name &rbrace;&rbrace;</b></nobr>,
			где
			<b>field_name</b> - название поля. Доступные поля:
			<ul>
				<li>
					Название организации: <nobr><b>&lbrace;&lbrace; company.name &rbrace;&rbrace;</b></nobr>
				</li>
				<li>
					Контр-агент:
					<ol>
						<li>
							Полное название: <nobr><b>&lbrace;&lbrace; agent.fullname &rbrace;&rbrace;</b></nobr>
						</li>
						<li>
							Сокращенное название: <nobr
								><b>&lbrace;&lbrace; agent.shortname &rbrace;&rbrace;</b></nobr
							>
						</li>
						<li>ИНН: <nobr><b>&lbrace;&lbrace; agent.inn &rbrace;&rbrace;</b></nobr></li>
						<li>
							ФИО директора: <nobr><b>&lbrace;&lbrace; agent.management &rbrace;&rbrace;</b></nobr>
						</li>
					</ol>
				</li>
				<li>
					Тип предложения: <nobr><b>&lbrace;&lbrace; offerType &rbrace;&rbrace;</b></nobr>
				</li>
				<li>
					Данные коммерческого предложения: <nobr
						><b>&lbrace;&lbrace; offerData &rbrace;&rbrace;</b></nobr
					>

					Поля внутри строк предложения:
					<ul>
						<li>
							Порядковый номер: <nobr><b>&lbrace;&lbrace; item.num &rbrace;&rbrace;</b></nobr>
						</li>
						<li>Название: <nobr><b>&lbrace;&lbrace; item.name &rbrace;&rbrace;</b></nobr></li>
						<li>
							Код ФККО (Только в КП на отходы): <nobr
								><b>&lbrace;&lbrace; item.name &rbrace;&rbrace;</b></nobr
							>
						</li>
						<li>
							Единица измерения: <nobr><b>&lbrace;&lbrace; item.unit &rbrace;&rbrace;</b></nobr>
						</li>
						<li>Цена: <nobr><b>&lbrace;&lbrace; item.price &rbrace;&rbrace;</b></nobr></li>
						<li>Количество: <nobr><b>&lbrace;&lbrace; item.amount &rbrace;&rbrace;</b></nobr></li>
						<li>Сумма: <nobr><b>&lbrace;&lbrace; item.sum &rbrace;&rbrace;</b></nobr></li>
					</ul>
				</li>
				<li>
					Общая стоимость предложения: <nobr
						><b>&lbrace;&lbrace; offerTotal &rbrace;&rbrace;</b></nobr
					>
				</li>
				<li>
					Автор документа: <nobr><b>&lbrace;&lbrace; author.name &rbrace;&rbrace;</b></nobr>
				</li>
				<li>
					Дата создания: <nobr><b>&lbrace;&lbrace; date &rbrace;&rbrace;</b></nobr>
				</li>
			</ul>
		</li>
		<li>Сохранить документ.</li>
		<li>Загрузить документ в систему.</li>
	</ol>

	<p>После загрузки документа он будет доступен для выбора при создании договора.</p>

	<p>
		Вы можете использовать документы <nobr><b>"Пример - КП на отходы"</b></nobr> и
		<nobr><b>"Пример - Общее КП"</b></nobr> в качестве шаблоны, скопировав нужные части оттуда.
	</p>
</div>
